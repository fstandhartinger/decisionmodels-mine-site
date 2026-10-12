"""HTTP API (stdlib ThreadingHTTPServer, JSON in/out). Listens on loopback behind nginx."""
from collections import defaultdict, deque
from datetime import datetime, timezone
import hashlib
import hmac
import ipaddress
import json
import logging
import re
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from . import AGREEMENT_VERSION, render, store as store_mod
from .config import Settings
from .pdfdoc import PdfError, build_pdf
from .validation import (LANGS, ValidationError, validate_accept, validate_contact, validate_preview)

log = logging.getLogger('mine_eu')
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
VERIFY_STATUSES = ('verified', 'rejected', 'pending')


class HttpError(Exception):
    def __init__(self, status, code, message='', **extra):
        super().__init__(message or code)
        self.status, self.code, self.message, self.extra = status, code, message or code, extra


class PreviewLimiter:
    """In-memory sliding window; preview stores nothing, this only bounds CPU."""

    def __init__(self, per_minute):
        self.per_minute = per_minute
        self.hits = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, ip):
        now = time.monotonic()
        with self.lock:
            q = self.hits[ip]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= self.per_minute:
                return False
            q.append(now)
            if len(self.hits) > 5000:
                for k in [k for k, v in self.hits.items() if not v or now - v[-1] > 60]:
                    del self.hits[k]
            return True


class App:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.store = store_mod.Store(settings.database_url, settings.rate_per_ip_hour, settings.rate_global_day)
        self.preview_limiter = PreviewLimiter(settings.preview_per_minute)

    def template(self, lang):
        try:
            return render.load_template(self.settings.legal_dir, lang)
        except render.TemplateError as exc:
            log.error('template error: %s', exc)
            raise HttpError(500, 'template_error', 'Agreement template unavailable.')


def _admin_ok(app, header):
    expected = app.settings.admin_token
    if not expected:
        raise HttpError(503, 'admin_disabled', 'Admin token not configured.')
    given = header[7:] if header.startswith('Bearer ') else ''
    # Compare fixed-length digests so neither length nor content leak through timing.
    if not hmac.compare_digest(hashlib.sha256(given.encode()).digest(), hashlib.sha256(expected.encode()).digest()):
        raise HttpError(401, 'unauthorized', 'Missing or invalid admin token.')


def _now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def pdf_for(app, row):
    record = dict(row)
    try:
        return build_pdf(record, app.settings)
    except PdfError as exc:
        log.error('pdf error: %s', exc)
        raise HttpError(500, 'pdf_error', 'PDF generation failed.')


class Handler(BaseHTTPRequestHandler):
    server_version = 'mine-eu'
    sys_version = ''
    protocol_version = 'HTTP/1.1'
    app: App = None  # set by make_server

    # ---- plumbing -----------------------------------------------------------------------------
    def log_message(self, fmt, *args):  # nginx already logs access; never log URLs (PDF tokens)
        pass

    def client_ip(self):
        peer = self.client_address[0]
        if peer in ('127.0.0.1', '::1'):  # only nginx on loopback may set X-Real-IP
            real = self.headers.get('X-Real-IP', '').strip()
            try:
                return str(ipaddress.ip_address(real))
            except ValueError:
                pass
        return peer

    def _send(self, status, body, ctype, extra=None):
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, obj):
        self._send(status, json.dumps(obj, ensure_ascii=False).encode('utf-8'), 'application/json; charset=utf-8')

    def _body(self):
        try:
            n = int(self.headers.get('Content-Length', ''))
        except ValueError:
            raise HttpError(411, 'length_required', 'Content-Length required.')
        if n > self.app.settings.max_body:
            raise HttpError(413, 'too_large', 'Request body too large.')
        if 'application/json' not in self.headers.get('Content-Type', ''):
            raise HttpError(415, 'unsupported_media_type', 'Use application/json.')
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode('utf-8'))
        except (UnicodeDecodeError, ValueError):
            raise HttpError(400, 'bad_json', 'Body is not valid JSON.')

    def _dispatch(self, method):
        try:
            parts = urlsplit(self.path)
            path, query = parts.path, parse_qs(parts.query)
            if not path.startswith('/api/eu/'):
                raise HttpError(404, 'not_found')
            self.route(method, path[len('/api/eu/'):], query)
        except HttpError as e:
            self.close_connection = True  # request body may be unread
            self._json(e.status, dict(error=e.code, message=e.message, **e.extra))
        except ValidationError as e:
            self._json(422, {'error': 'validation_failed', 'message': e.message, 'fields': e.fields})
        except store_mod.DbUnavailable:
            self._json(503, {'error': 'db_unavailable', 'message': 'Storage temporarily unavailable.'})
        except store_mod.RateLimited:
            self._json(429, {'error': 'rate_limited', 'message': 'Too many submissions; please try again later.'})
        except store_mod.NotFound:
            self._json(404, {'error': 'not_found'})
        except store_mod.Conflict as e:
            self._json(409, {'error': 'conflict', 'message': str(e)})
        except Exception as e:  # never leak details; no personal data in log
            log.error('unhandled %s', type(e).__name__, exc_info=True)
            self._json(500, {'error': 'internal_error'})

    def do_GET(self):
        self._dispatch('GET')

    def do_POST(self):
        self._dispatch('POST')

    # ---- routing ------------------------------------------------------------------------------
    def route(self, method, path, query):
        app = self.app
        if path == 'health':
            self._need(method, 'GET')
            try:
                app.store.ping()
                return self._json(200, {'db': True})
            except store_mod.DbUnavailable:
                return self._json(503, {'db': False})
        if path == 'agreement':
            self._need(method, 'GET')
            lang = query.get('lang', ['en'])[0]
            if lang not in LANGS:
                raise ValidationError({'lang': 'Must be "en" or "de".'})
            text, sha = app.template(lang)
            return self._json(200, {'version': AGREEMENT_VERSION, 'lang': lang, 'template_sha256': sha, 'text': text})
        if path == 'preview':
            self._need(method, 'POST')
            if not app.preview_limiter.allow(self.client_ip()):
                raise store_mod.RateLimited()
            lang, fields = validate_preview(self._body())
            template, _ = app.template(lang)
            text = self._render(render.render_for_hash, template, fields, lang)
            return self._json(200, {'text': text, 'text_sha256': render.sha256_text(text)})
        if path == 'accept':
            self._need(method, 'POST')
            return self._accept()
        if path == 'contact':
            self._need(method, 'POST')
            data = validate_contact(self._body())
            iid = app.store.create_inquiry(data, self.client_ip(), self.headers.get('User-Agent', ''))
            log.info('write kind=inquiry id=%s status=received', iid)
            return self._json(201, {'inquiry_id': iid, 'status': 'received'})
        m = re.fullmatch(r'agreements/([0-9a-f-]{36})\.pdf', path)
        if m:
            self._need(method, 'GET')
            if not UUID_RE.match(m.group(1)):
                raise HttpError(404, 'not_found')
            row = app.store.get_agreement_for_token(m.group(1), query.get('t', [''])[0])
            return self._pdf(row)
        if path.startswith('admin/'):
            return self._admin(method, path[len('admin/'):], query)
        raise HttpError(404, 'not_found')

    def _need(self, method, expected):
        if method != expected:
            raise HttpError(405, 'method_not_allowed', f'Use {expected}.')

    @staticmethod
    def _render(fn, *args):
        try:
            return fn(*args)
        except render.TemplateError as exc:
            log.error('template error: %s', exc)
            raise HttpError(500, 'template_error', 'Agreement template is invalid.')

    def _accept(self):
        app = self.app
        lang, fields, claimed = validate_accept(self._body())
        template, template_sha = app.template(lang)
        text_hashed = self._render(render.render_for_hash, template, fields, lang)
        sha = render.sha256_text(text_hashed)
        if not hmac.compare_digest(sha, claimed):
            raise HttpError(409, 'text_changed',
                            'The agreement text differs from what you reviewed; please review it again.',
                            text_sha256=sha)
        agreement_id = str(uuid.uuid4())
        accepted_at = _now_iso()
        final = self._render(render.render_final, template, fields, lang, agreement_id, accepted_at, sha)
        token = app.store.create_agreement(
            lang=lang, version=AGREEMENT_VERSION, template_sha256=template_sha, text_sha256=sha,
            text_hashed=text_hashed, rendered_text=final, fields=fields,
            accepted_at=accepted_at, agreement_id=agreement_id, client_ip=self.client_ip(),
            user_agent=self.headers.get('User-Agent', ''))
        log.info('write kind=agreement id=%s status=signed', agreement_id)
        self._json(201, {'agreement_id': agreement_id, 'status': 'signed',
                         'pdf_url': f'/api/eu/agreements/{agreement_id}.pdf?t={token}'})

    def _pdf(self, row):
        body = pdf_for(self.app, row)
        self._send(200, body, 'application/pdf',
                   {'Content-Disposition': f'attachment; filename="agreement-{row["agreement_id"]}.pdf"'})

    def _admin(self, method, path, query):
        app = self.app
        _admin_ok(app, self.headers.get('Authorization', ''))
        if path == 'events':
            self._need(method, 'GET')
            try:
                after = int(query.get('after', ['0'])[0])
                limit = min(int(query.get('limit', ['100'])[0]), 500)
            except ValueError:
                raise ValidationError({'after': 'Must be an integer.'})
            if after < 0 or limit < 1:
                raise ValidationError({'after': 'Must be non-negative.'})
            events, cursor = app.store.events(after, limit)
            return self._json(200, {'events': events, 'cursor': cursor})
        if path == 'registry':
            self._need(method, 'GET')
            return self._json(200, {'miners': app.store.registry()})
        m = re.fullmatch(r'agreements/([0-9a-f-]{36})(\.pdf|/verification|/revoke)', path)
        if not m or not UUID_RE.match(m.group(1)):
            raise HttpError(404, 'not_found')
        aid, what = m.groups()
        if what == '.pdf':
            self._need(method, 'GET')
            return self._pdf(app.store.get_agreement(aid))
        self._need(method, 'POST')
        data = self._body()
        if not isinstance(data, dict):
            raise ValidationError({'_': 'Body must be a JSON object.'})
        if what == '/verification':
            unknown = set(data) - {'status', 'checks', 'note'}
            if unknown:
                raise ValidationError({k: 'Unknown field.' for k in sorted(unknown)[:10]})
            status = data.get('status')
            if status not in VERIFY_STATUSES:
                raise ValidationError({'status': 'Must be one of: ' + ', '.join(VERIFY_STATUSES)})
            checks = data.get('checks', {})
            note = data.get('note', '')
            if (not isinstance(checks, dict) or len(json.dumps(checks)) > 8000
                    or not all(isinstance(k, str) and isinstance(v, (bool, int, float, str, type(None)))
                               for k, v in checks.items())):
                raise ValidationError({'checks': 'Must be a flat object of scalars, at most 8000 bytes.'})
            if not isinstance(note, str) or len(note) > 2000:
                raise ValidationError({'note': 'At most 2000 characters.'})
            v = app.store.set_verification(aid, status, checks, note)
            log.info('write kind=verification id=%s status=%s', aid, status)
            return self._json(200, {'agreement_id': aid, 'verification': v})
        unknown = set(data) - {'reason'}
        reason = data.get('reason', '')
        if unknown or not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
            raise ValidationError({'reason': 'Required, at most 1000 characters.'})
        app.store.revoke(aid, reason.strip())
        log.info('write kind=revocation id=%s status=revoked', aid)
        self._json(200, {'agreement_id': aid, 'status': 'revoked'})


def make_server(settings: Settings, app: App = None):
    app = app or App(settings)
    handler = type('BoundHandler', (Handler,), {'app': app})
    srv = ThreadingHTTPServer((settings.host, settings.port), handler)
    srv.daemon_threads = True
    srv.app = app
    return srv


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logging.getLogger('fontTools').setLevel(logging.WARNING)
    settings = Settings.from_env()
    srv = make_server(settings)
    try:  # best effort; the first request retries
        if srv.app.store.configured:
            srv.app.store.ensure_schema()
    except Exception as e:
        log.warning('schema not ready at start: %s', type(e).__name__)
    log.info('listening on %s:%s db=%s admin=%s', settings.host, settings.port,
             'yes' if settings.database_url else 'no', 'yes' if settings.admin_token else 'no')
    srv.serve_forever()
