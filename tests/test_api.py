"""EU-miner agreement API: validation, rendering, PDF, and an end-to-end flow against a throwaway Postgres.

DB tests use TEST_PG_ADMIN_URL (default: local unix socket, database "postgres"), create a temporary
database named mine_eu_test_<random> and drop it afterwards. They never touch DATABASE_URL.
"""
import json
import logging
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import threading
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

try:
    import psycopg
    import fpdf  # noqa: F401
    HAVE_DEPS = True
except ImportError:  # the static-site checks run without the API dependencies
    HAVE_DEPS = False

if HAVE_DEPS:
    from mine_eu import AGREEMENT_VERSION, render
    from mine_eu.config import Settings
    from mine_eu.pdfdoc import build_pdf
    from mine_eu.server import make_server
    from mine_eu.validation import (ValidationError, validate_accept, validate_contact, validate_preview)

HK1 = '5' + 'F' * 47
HK2 = '5' + 'G' * 47
ADMIN = 'test-admin-token-' + secrets.token_hex(8)
ADMIN_URL = os.environ.get('TEST_PG_ADMIN_URL', 'host=/var/run/postgresql dbname=postgres')


def payload(**over):
    p = dict(lang='en', miner_company='Müller GmbH', miner_legal_form='GmbH', miner_address='Hauptstraße 1\n80331 München',
             miner_country='de', miner_register='HRB 123456, AG München', miner_vat_id='DE123456789',
             signatory_name='Anna Müller', signatory_role='Geschäftsführerin', signatory_email='anna@mueller.example',
             privacy_contact='datenschutz@mueller.example',
             dc_locations=[{'provider': 'Hetzner', 'city': 'Falkenstein', 'country': 'DE'}],
             hotkeys=[HK1], endpoints=['miner.mueller.example:8443'],
             own_subprocessors=[{'name': 'Hetzner Online GmbH', 'service': 'Hosting', 'location': 'Falkenstein, DE'}],
             tom_statement='Encrypted disks.\nAccess limited to two admins.')
    p.update(over)
    return p


def accept_payload(sha, **over):
    p = payload(text_sha256=sha, authority_confirmed=True, terms_read=True, website='')
    p.update(over)
    return p


@unittest.skipUnless(HAVE_DEPS, 'psycopg/fpdf2 not installed')
class UnitTests(unittest.TestCase):
    def test_valid_payload_normalised(self):
        lang, f = validate_preview(payload())
        self.assertEqual(lang, 'en')
        self.assertEqual(f['miner_country'], 'DE')
        self.assertEqual(f['miner_address'], 'Hauptstraße 1, 80331 München')

    def test_non_eu_country_rejected_with_clear_message(self):
        with self.assertRaises(ValidationError) as cm:
            validate_preview(payload(miner_country=''))
        self.assertEqual(cm.exception.fields['miner_country'], 'This field is required.')
        for code in ('US', 'GB', 'CH', 'XX', 'Germany'):
            with self.assertRaises(ValidationError) as cm:
                validate_preview(payload(miner_country=code))
            self.assertIn('EU/EEA', cm.exception.fields['miner_country'])
        for code in ('NO', 'IS', 'LI', 'fr', 'SE'):
            validate_preview(payload(miner_country=code))
        with self.assertRaises(ValidationError) as cm:
            validate_preview(payload(dc_locations=[{'provider': 'X', 'city': 'NYC', 'country': 'US'}]))
        self.assertIn('dc_locations[0].country', cm.exception.fields)

    def test_hotkeys_endpoints_and_unknown_fields(self):
        with self.assertRaises(ValidationError) as cm:
            validate_preview(payload(hotkeys=['5abc', '6' + 'F' * 47, '5' + '0' * 47]))
        self.assertEqual({'hotkeys[0]', 'hotkeys[1]', 'hotkeys[2]'}, set(cm.exception.fields))
        with self.assertRaises(ValidationError) as cm:
            validate_preview(payload(endpoints=['nohost', 'a.b:99999', 'x y:80']))
        self.assertEqual(3, len(cm.exception.fields))
        validate_preview(payload(endpoints=['[2001:db8::1]:443', '203.0.113.7:8080'], hotkeys=[]))
        validate_preview(payload(website=''))  # the form always sends the (empty) honeypot
        with self.assertRaises(ValidationError):
            validate_preview(payload(website='bot'))
        with self.assertRaises(ValidationError) as cm:
            validate_preview(payload(surprise='x'))
        self.assertIn('surprise', cm.exception.fields)

    def test_lengths_and_required(self):
        with self.assertRaises(ValidationError) as cm:
            validate_preview(payload(miner_company='x' * 201, tom_statement='y' * 4001, dc_locations=[]))
        self.assertTrue({'miner_company', 'tom_statement', 'dc_locations'} <= set(cm.exception.fields))
        with self.assertRaises(ValidationError):
            validate_preview(payload(signatory_name='bad\x00name'))
        with self.assertRaises(ValidationError):
            validate_preview(payload(signatory_name='multi\nline'))
        with self.assertRaises(ValidationError):
            validate_preview(payload(hotkeys=[HK1] * 1 + ['5' + 'H' * 47] * 51))

    def test_accept_requires_confirmations_and_empty_honeypot(self):
        sha = 'a' * 64
        validate_accept(accept_payload(sha))
        for bad in (dict(authority_confirmed=False), dict(terms_read='yes'), dict(text_sha256='zz'), dict(website='http://spam')):
            with self.assertRaises(ValidationError):
                validate_accept(accept_payload(sha, **bad))
        with self.assertRaises(ValidationError):
            validate_contact(dict(company='A', name='B', email='nope', website=''))
        with self.assertRaises(ValidationError):
            validate_contact(dict(company='A', name='B', email='b@a.example', website='spam'))

    def test_templates_use_only_known_placeholders(self):
        for lang in ('en', 'de'):
            text, sha = render.load_template(ROOT / 'legal', lang)
            self.assertLessEqual(render.template_placeholders(text), render.KNOWN_KEYS, lang)
            self.assertEqual(len(sha), 64)

    def test_render_hash_and_final(self):
        _, f = validate_preview(payload())
        tpl, _ = render.load_template(ROOT / 'legal', 'en')
        hashed = render.render_for_hash(tpl, f, 'en')
        self.assertEqual(hashed, render.render_for_hash(tpl, f, 'en'))
        self.assertIn('[assigned on acceptance]', hashed)
        self.assertIn('Müller GmbH', hashed)
        self.assertIn('> Encrypted disks.\n> Access limited', hashed)
        sha = render.sha256_text(hashed)
        final = render.render_final(tpl, f, 'en', 'AID', '2026-10-12T10:00:00Z', sha)
        self.assertIn('AID', final)
        self.assertIn(sha, final)
        self.assertNotIn('[assigned on acceptance]', final)
        # one-pass substitution: a placeholder typed into a field is not expanded again
        _, f2 = validate_preview(payload(miner_company='{{hotkeys}}'))
        self.assertIn('{{hotkeys}}', render.render_for_hash(tpl, f2, 'en'))

    def _record(self, lang='en'):
        _, f = validate_preview(payload(lang=lang))
        tpl, _ = render.load_template(ROOT / 'legal', lang)
        hashed = render.render_for_hash(tpl, f, lang)
        sha = render.sha256_text(hashed)
        aid = '11111111-2222-4333-8444-555555555555'
        at = '2026-10-12T10:00:00Z'
        return dict(agreement_id=aid, lang=lang, version=AGREEMENT_VERSION, fields=f, accepted_at=at,
                    client_ip='203.0.113.9', text_sha256=sha, rendered_text=render.render_final(tpl, f, lang, aid, at, sha))

    def test_pdf_umlauts_and_determinism(self):
        s = Settings()
        with self.assertLogs('fpdf', level='WARNING') as logs:  # missing glyphs would warn
            logging.getLogger('fpdf').warning('sentinel')
            pdf = build_pdf(self._record('de'), s)
        self.assertEqual([r for r in logs.output if 'sentinel' not in r], [])
        self.assertTrue(pdf.startswith(b'%PDF'))
        self.assertEqual(pdf, build_pdf(self._record('de'), s))
        self.assertGreater(len(pdf), 5000)
        tool = shutil.which('pdftotext')
        if tool:
            out = subprocess.run([tool, '-layout', '-', '-'], input=pdf, capture_output=True, check=True).stdout.decode()
            self.assertIn('Müller GmbH', out)
            self.assertIn('München', out)
            self.assertIn('Art. 28 Abs. 9 DSGVO', out)
            self.assertIn('11111111-2222-4333-8444-555555555555', out)
            en = subprocess.run([tool, '-layout', '-', '-'], input=build_pdf(self._record('en'), s),
                                capture_output=True, check=True).stdout.decode()
            self.assertIn("Accepted electronically by the Miner's authorised signatory (Art. 28(9) GDPR)", en)
            self.assertIn('https://mine.decisionmodels.io/eu', en)

    def test_pdf_handles_tables_and_long_text(self):
        rec = self._record()
        rec['rendered_text'] += '\n\n| Col A | Col B |\n| --- | --- |\n| ü | **bold** |\n\n' + 'Lorem ipsum. ' * 800
        pdf = build_pdf(rec, Settings())
        self.assertTrue(pdf.startswith(b'%PDF'))


def _create_db():
    name = 'mine_eu_test_' + secrets.token_hex(6)
    with psycopg.connect(ADMIN_URL, autocommit=True, connect_timeout=3) as c:
        c.execute(f'create database {name}')
    return name


def _drop_db(name):
    with psycopg.connect(ADMIN_URL, autocommit=True) as c:
        c.execute(f'drop database if exists {name} with (force)')


def _db_url(name):
    if '://' in ADMIN_URL:
        head, _, _ = ADMIN_URL.rpartition('/')
        return head + '/' + name
    return ADMIN_URL.replace('dbname=postgres', 'dbname=' + name)


def call(base, method, path, body=None, headers=None, raw=False):
    data = json.dumps(body).encode() if body is not None else None
    h = {'Content-Type': 'application/json', 'X-Real-IP': '198.51.100.1'}
    h.update(headers or {})
    req = urllib.request.Request(base + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            payload_ = r.read()
            return r.status, (payload_ if raw else json.loads(payload_))
    except urllib.error.HTTPError as e:
        payload_ = e.read()
        try:
            return e.code, json.loads(payload_)
        except ValueError:
            return e.code, payload_


def admin(token=ADMIN):
    return {'Authorization': 'Bearer ' + token}


@unittest.skipUnless(HAVE_DEPS, 'psycopg/fpdf2 not installed')
class ApiFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.db = _create_db()
        except Exception as exc:  # no local Postgres available
            raise unittest.SkipTest(f'no throwaway Postgres: {type(exc).__name__}')
        s = Settings(database_url=_db_url(cls.db), admin_token=ADMIN, port=0, legal_dir=ROOT / 'legal',
                     rate_per_ip_hour=5, rate_global_day=50)
        cls.srv = make_server(s)
        cls.thread = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:%d/api/eu/' % cls.srv.server_address[1]
        cls.root = cls.base[:-len('api/eu/')]

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        _drop_db(cls.db)

    def url(self, path):
        return self.base[:-len('api/eu/')] + path.lstrip('/')

    def test_01_health_and_agreement(self):
        self.assertEqual(call(self.base, 'GET', 'health'), (200, {'db': True}))
        st, body = call(self.base, 'GET', 'agreement?lang=de')
        self.assertEqual(st, 200)
        self.assertEqual((body['version'], body['lang']), (AGREEMENT_VERSION, 'de'))
        self.assertIn('{{miner_company}}', body['text'])
        self.assertEqual(call(self.base, 'GET', 'agreement?lang=fr')[0], 422)

    def test_02_full_flow(self):
        st, pv = call(self.base, 'POST', 'preview', payload(hotkeys=[HK1, HK2]))
        self.assertEqual(st, 200)
        self.assertEqual(pv['text_sha256'], render.sha256_text(pv['text']))
        self.assertIn('Müller GmbH', pv['text'])
        # tampered hash -> 409, nothing stored
        st, err = call(self.base, 'POST', 'accept', accept_payload('0' * 64, hotkeys=[HK1, HK2]), {'X-Real-IP': '198.51.100.20'})
        self.assertEqual((st, err['error']), (409, 'text_changed'))
        # changed field after review -> 409
        st, err = call(self.base, 'POST', 'accept',
                       accept_payload(pv['text_sha256'], miner_company='Other GmbH', hotkeys=[HK1, HK2]),
                       {'X-Real-IP': '198.51.100.20'})
        self.assertEqual(st, 409)
        st, acc = call(self.base, 'POST', 'accept', accept_payload(pv['text_sha256'], hotkeys=[HK1, HK2]),
                       {'X-Real-IP': '198.51.100.20'})
        self.assertEqual((st, acc['status']), (201, 'signed'))
        aid = acc['agreement_id']
        self.assertTrue(acc['pdf_url'].startswith(f'/api/eu/agreements/{aid}.pdf?t='))
        st, pdf = call(self.root, 'GET', acc['pdf_url'][1:], raw=True)
        self.assertEqual(st, 200)
        self.assertTrue(pdf.startswith(b'%PDF'))
        # token check
        self.assertEqual(call(self.root, 'GET', f'api/eu/agreements/{aid}.pdf?t=wrong')[0], 404)
        self.assertEqual(call(self.root, 'GET', f'api/eu/agreements/{aid}.pdf')[0], 404)
        # events
        self.assertEqual(call(self.base, 'GET', 'admin/events')[0], 401)
        self.assertEqual(call(self.base, 'GET', 'admin/events', headers=admin('nope'))[0], 401)
        st, ev = call(self.base, 'GET', 'admin/events?after=0', headers=admin())
        self.assertEqual(st, 200)
        mine = [e for e in ev['events'] if e.get('agreement_id') == aid]
        self.assertEqual(len(mine), 1)
        self.assertEqual(mine[0]['kind'], 'agreement')
        self.assertEqual(mine[0]['hotkeys'], [HK1, HK2])
        self.assertEqual(call(self.base, 'GET', f'admin/events?after={ev["cursor"]}', headers=admin())[1]['events'], [])
        st, apdf = call(self.root, 'GET', mine[0]['admin_pdf_path'][1:], headers=admin(), raw=True)
        self.assertEqual((st, apdf[:4]), (200, b'%PDF'))
        # registry empty until verified
        st, reg = call(self.base, 'GET', 'admin/registry', headers=admin())
        self.assertEqual([m for m in reg['miners'] if m['agreement_id'] == aid], [])
        st, v = call(self.base, 'POST', f'admin/agreements/{aid}/verification',
                     {'status': 'verified', 'checks': {'vat': True, 'hotkey_signature': True}, 'note': 'ok'}, admin())
        self.assertEqual((st, v['verification']['status']), (200, 'verified'))
        st, reg = call(self.base, 'GET', 'admin/registry', headers=admin())
        entry = [m for m in reg['miners'] if m['agreement_id'] == aid][0]
        self.assertEqual(entry['hotkeys'], [HK1, HK2])
        self.assertEqual(entry['dc_countries'], ['DE'])
        self.assertTrue(entry['routing_eligible'])
        self.assertEqual(call(self.base, 'POST', f'admin/agreements/{aid}/verification', {'status': 'maybe'}, admin())[0], 422)
        # revoke -> no longer eligible, further verification refused
        self.assertEqual(call(self.base, 'POST', f'admin/agreements/{aid}/revoke', {'reason': ''}, admin())[0], 422)
        self.assertEqual(call(self.base, 'POST', f'admin/agreements/{aid}/revoke', {'reason': 'left network'}, admin())[0], 200)
        entry = [m for m in call(self.base, 'GET', 'admin/registry', headers=admin())[1]['miners'] if m['agreement_id'] == aid][0]
        self.assertFalse(entry['routing_eligible'])
        self.assertTrue(entry['revoked'])
        self.assertEqual(call(self.base, 'POST', f'admin/agreements/{aid}/verification', {'status': 'verified'}, admin())[0], 409)
        # audit record
        import psycopg as pg
        with pg.connect(_db_url(self.db)) as c:
            row = c.execute('select client_ip, user_agent, status, text_sha256, token_sha256 from eu_agreements').fetchone()
        self.assertEqual(row[0], '198.51.100.20')
        self.assertEqual(row[2], 'revoked')
        self.assertEqual(row[3], pv['text_sha256'])
        self.assertEqual(len(row[4]), 64)
        self.assertNotIn(acc['pdf_url'].split('t=')[1], row)

    def test_03_validation_errors_over_http(self):
        st, err = call(self.base, 'POST', 'preview', payload(miner_country='US'))
        self.assertEqual(st, 422)
        self.assertIn('EU/EEA', err['fields']['miner_country'])
        st, _ = call(self.base, 'POST', 'accept', accept_payload('a' * 64, website='x'))
        self.assertEqual(st, 422)
        req = urllib.request.Request(self.base + 'preview', data=b'{not json', method='POST',
                                     headers={'Content-Type': 'application/json'})
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req)
        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(call(self.base, 'GET', 'nothing')[0], 404)
        self.assertEqual(call(self.base, 'GET', 'accept')[0], 405)

    def test_04_contact_and_events(self):
        st, r = call(self.base, 'POST', 'contact', dict(company='Acme', name='Bo', email='bo@acme.example', country='US',
                                                        gpus='8x4090', message='Hi', website=''),
                     {'X-Real-IP': '198.51.100.30'})
        self.assertEqual((st, r['status']), (201, 'received'))
        evs = call(self.base, 'GET', 'admin/events?after=0&limit=500', headers=admin())[1]['events']
        self.assertTrue(any(e.get('inquiry_id') == r['inquiry_id'] and e['company'] == 'Acme' for e in evs))

    def test_05_rate_limit_per_ip(self):
        ip = {'X-Real-IP': '198.51.100.99'}
        body = dict(company='Acme', name='Bo', email='bo@acme.example', country='', gpus='', message='', website='')
        codes = [call(self.base, 'POST', 'contact', body, ip)[0] for _ in range(6)]
        self.assertEqual(codes, [201] * 5 + [429])
        # another IP is unaffected
        self.assertEqual(call(self.base, 'POST', 'contact', body, {'X-Real-IP': '198.51.100.98'})[0], 201)

    def test_06_global_day_limit(self):
        from mine_eu.store import Store, RateLimited
        s = Store(_db_url(self.db), per_ip_hour=1000, global_day=3)
        s.ensure_schema()
        body = dict(company='A', name='B', email='b@a.example', country='', gpus='', message='')
        with psycopg.connect(_db_url(self.db)) as c:
            c.execute('delete from eu_rate_events')
        for i in range(3):
            s.create_inquiry(body, f'192.0.2.{i}', 'ua')
        with self.assertRaises(RateLimited):
            s.create_inquiry(body, '192.0.2.200', 'ua')

    def test_07_hotkey_conflict_flagged(self):
        ids = []
        for n, ip in enumerate(('198.51.100.41', '198.51.100.42')):
            p = payload(hotkeys=[HK2], miner_company=f'Dup {n} GmbH')
            sha = call(self.base, 'POST', 'preview', p)[1]['text_sha256']
            st, acc = call(self.base, 'POST', 'accept', dict(p, text_sha256=sha, authority_confirmed=True,
                                                            terms_read=True, website=''), {'X-Real-IP': ip})
            self.assertEqual(st, 201)
            ids.append(acc['agreement_id'])
            call(self.base, 'POST', f"admin/agreements/{acc['agreement_id']}/verification", {'status': 'verified'}, admin())
        reg = {m['agreement_id']: m for m in call(self.base, 'GET', 'admin/registry', headers=admin())[1]['miners']}
        self.assertEqual(reg[ids[0]]['hotkey_conflicts'], [HK2])
        self.assertEqual(reg[ids[1]]['hotkey_conflicts'], [HK2])


@unittest.skipUnless(HAVE_DEPS, 'psycopg/fpdf2 not installed')
class NoDatabase(unittest.TestCase):
    def test_static_ok_writes_503(self):
        s = Settings(database_url='', admin_token='', port=0, legal_dir=ROOT / 'legal')
        srv = make_server(s)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = 'http://127.0.0.1:%d/api/eu/' % srv.server_address[1]
        try:
            self.assertEqual(call(base, 'GET', 'health'), (503, {'db': False}))
            st, pv = call(base, 'POST', 'preview', payload())
            self.assertEqual(st, 200)  # preview needs no storage
            st, err = call(base, 'POST', 'accept', accept_payload(pv['text_sha256']))
            self.assertEqual((st, err['error']), (503, 'db_unavailable'))
            self.assertEqual(call(base, 'GET', 'admin/events', headers=admin())[0], 503)  # admin disabled
        finally:
            srv.shutdown()
            srv.server_close()


if __name__ == '__main__':
    unittest.main()
