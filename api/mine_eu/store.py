"""Postgres storage (psycopg 3, plain SQL). Schema is created idempotently on first use."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import secrets
import threading
import uuid

import psycopg
from psycopg.rows import dict_row

SCHEMA = """
create table if not exists eu_agreements (
  agreement_id uuid primary key,
  version text not null, lang text not null,
  template_sha256 text not null, text_sha256 text not null,
  text_hashed text not null, rendered_text text not null,
  fields jsonb not null,
  accepted_at timestamptz not null,
  client_ip text, user_agent text,
  status text not null default 'signed',
  token_sha256 text not null,
  verification jsonb, verified_at timestamptz,
  revoked_at timestamptz, revoked_reason text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table if not exists eu_agreement_hotkeys (
  agreement_id uuid not null references eu_agreements(agreement_id) on delete cascade,
  hotkey text not null,
  primary key (agreement_id, hotkey)
);
create index if not exists eu_agreement_hotkeys_hotkey on eu_agreement_hotkeys (hotkey);
create table if not exists eu_inquiries (
  id uuid primary key,
  company text not null, name text not null, email text not null,
  country text, gpus text, message text,
  client_ip text, user_agent text,
  created_at timestamptz not null default now()
);
create table if not exists eu_events (
  id bigserial primary key,
  kind text not null, ref_id uuid not null,
  created_at timestamptz not null default now()
);
create table if not exists eu_rate_events (
  id bigserial primary key,
  ip_hash text not null,
  created_at timestamptz not null default now()
);
create index if not exists eu_rate_events_ip on eu_rate_events (ip_hash, created_at);
create index if not exists eu_rate_events_at on eu_rate_events (created_at);
"""
LOCK_SCHEMA, LOCK_WRITE = 7360101, 7360102


class RateLimited(Exception):
    pass


class NotFound(Exception):
    pass


class Conflict(Exception):
    pass


class DbUnavailable(Exception):
    pass


def iso(dt):
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if dt else None


def hash_token(token):
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


class Store:
    def __init__(self, database_url, per_ip_hour=5, global_day=50):
        self.url = database_url
        self.per_ip_hour = per_ip_hour
        self.global_day = global_day
        self._ready = False
        self._lock = threading.Lock()

    @property
    def configured(self):
        return bool(self.url)

    @contextmanager
    def conn(self):
        if not self.url:
            raise DbUnavailable('DATABASE_URL not set')
        try:
            with psycopg.connect(self.url, connect_timeout=8, row_factory=dict_row) as c:
                yield c
        except psycopg.OperationalError as exc:
            raise DbUnavailable(type(exc).__name__) from exc

    def ensure_schema(self):
        if self._ready:
            return
        with self._lock:
            if self._ready:
                return
            with self.conn() as c:
                c.execute('select pg_advisory_xact_lock(%s)', (LOCK_SCHEMA,))
                c.execute(SCHEMA)
            self._ready = True

    def ping(self):
        with self.conn() as c:
            c.execute('select 1')
        return True

    # ---- writes -------------------------------------------------------------------------------
    def _check_rate(self, c, ip):
        ip_hash = hashlib.sha256(('mine-eu|' + (ip or '')).encode()).hexdigest()
        c.execute('select pg_advisory_xact_lock(%s)', (LOCK_WRITE,))
        c.execute("delete from eu_rate_events where created_at < now() - interval '2 days'")
        n_ip = c.execute("select count(*) as n from eu_rate_events where ip_hash=%s and created_at > now() - interval '1 hour'",
                         (ip_hash,)).fetchone()['n']
        n_all = c.execute("select count(*) as n from eu_rate_events where created_at > now() - interval '1 day'").fetchone()['n']
        if n_ip >= self.per_ip_hour or n_all >= self.global_day:
            raise RateLimited()
        c.execute('insert into eu_rate_events (ip_hash) values (%s)', (ip_hash,))

    def create_agreement(self, *, lang, version, template_sha256, text_sha256, text_hashed, rendered_text,
                         fields, accepted_at, agreement_id, client_ip, user_agent):
        """Stores a signed agreement; returns the plaintext PDF token (only its hash is kept)."""
        self.ensure_schema()
        token = secrets.token_urlsafe(32)
        with self.conn() as c:
            self._check_rate(c, client_ip)
            c.execute(
                """insert into eu_agreements (agreement_id, version, lang, template_sha256, text_sha256, text_hashed,
                   rendered_text, fields, accepted_at, client_ip, user_agent, status, token_sha256)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'signed',%s)""",
                (agreement_id, version, lang, template_sha256, text_sha256, text_hashed, rendered_text,
                 json.dumps(fields), accepted_at, client_ip, (user_agent or '')[:300], hash_token(token)))
            for hk in fields['hotkeys']:
                c.execute('insert into eu_agreement_hotkeys (agreement_id, hotkey) values (%s,%s)', (agreement_id, hk))
            c.execute("insert into eu_events (kind, ref_id) values ('agreement', %s)", (agreement_id,))
        return token

    def create_inquiry(self, data, client_ip, user_agent):
        self.ensure_schema()
        inquiry_id = str(uuid.uuid4())
        with self.conn() as c:
            self._check_rate(c, client_ip)
            c.execute(
                """insert into eu_inquiries (id, company, name, email, country, gpus, message, client_ip, user_agent)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (inquiry_id, data['company'], data['name'], data['email'], data['country'], data['gpus'],
                 data['message'], client_ip, (user_agent or '')[:300]))
            c.execute("insert into eu_events (kind, ref_id) values ('inquiry', %s)", (inquiry_id,))
        return inquiry_id

    # ---- reads --------------------------------------------------------------------------------
    def get_agreement(self, agreement_id):
        self.ensure_schema()
        with self.conn() as c:
            row = c.execute('select * from eu_agreements where agreement_id=%s', (agreement_id,)).fetchone()
        if not row:
            raise NotFound()
        row['agreement_id'] = str(row['agreement_id'])
        row['accepted_at'] = iso(row['accepted_at'])
        return row

    def get_agreement_for_token(self, agreement_id, token):
        row = self.get_agreement(agreement_id)
        if not hmac.compare_digest(row['token_sha256'], hash_token(token or '')):
            raise NotFound()
        return row

    def events(self, after, limit):
        self.ensure_schema()
        with self.conn() as c:
            evs = c.execute('select id, kind, ref_id, created_at from eu_events where id > %s order by id limit %s',
                            (after, limit)).fetchall()
            out = []
            for e in evs:
                item = {'id': e['id'], 'kind': e['kind'], 'created_at': iso(e['created_at'])}
                if e['kind'] == 'agreement':
                    a = c.execute('select agreement_id, fields, lang, version, accepted_at, status from eu_agreements '
                                  'where agreement_id=%s', (e['ref_id'],)).fetchone()
                    if not a:
                        continue
                    f = a['fields']
                    item.update(agreement_id=str(a['agreement_id']), miner_company=f['miner_company'],
                                miner_country=f['miner_country'], signatory_name=f['signatory_name'],
                                signatory_email=f['signatory_email'], privacy_contact=f['privacy_contact'],
                                hotkeys=f['hotkeys'], endpoints=f['endpoints'],
                                dc_countries=sorted({d['country'] for d in f['dc_locations']}),
                                lang=a['lang'], version=a['version'], status=a['status'],
                                accepted_at=iso(a['accepted_at']),
                                admin_pdf_path=f"/api/eu/admin/agreements/{a['agreement_id']}.pdf")
                else:
                    q = c.execute('select * from eu_inquiries where id=%s', (e['ref_id'],)).fetchone()
                    if not q:
                        continue
                    item.update(inquiry_id=str(q['id']), company=q['company'], name=q['name'], email=q['email'],
                                country=q['country'], gpus=q['gpus'], message=q['message'])
                out.append(item)
        cursor = evs[-1]['id'] if evs else after
        return out, cursor

    # ---- admin updates ------------------------------------------------------------------------
    def set_verification(self, agreement_id, status, checks, note):
        self.ensure_schema()
        now = datetime.now(timezone.utc)
        verification = {'status': status, 'checks': checks, 'note': note, 'updated_at': iso(now)}
        with self.conn() as c:
            row = c.execute('select status from eu_agreements where agreement_id=%s for update', (agreement_id,)).fetchone()
            if not row:
                raise NotFound()
            if row['status'] == 'revoked':
                raise Conflict('agreement is revoked')
            c.execute('update eu_agreements set verification=%s, verified_at=%s, updated_at=now() where agreement_id=%s',
                      (json.dumps(verification), now if status == 'verified' else None, agreement_id))
        return verification

    def revoke(self, agreement_id, reason):
        self.ensure_schema()
        with self.conn() as c:
            row = c.execute('select status from eu_agreements where agreement_id=%s for update', (agreement_id,)).fetchone()
            if not row:
                raise NotFound()
            c.execute("update eu_agreements set status='revoked', revoked_at=now(), revoked_reason=%s, "
                      "updated_at=now() where agreement_id=%s", (reason, agreement_id))

    def registry(self):
        self.ensure_schema()
        with self.conn() as c:
            rows = c.execute("""select agreement_id, fields, status, verified_at, revoked_at
                                from eu_agreements where verification->>'status' = 'verified'
                                order by created_at""").fetchall()
            out = []
            for r in rows:
                f = r['fields']
                conflicts = [x['hotkey'] for x in c.execute(
                    """select distinct h.hotkey from eu_agreement_hotkeys h
                       join eu_agreements a using (agreement_id)
                       where h.hotkey = any(%s) and h.agreement_id <> %s and a.status <> 'revoked'""",
                    (f['hotkeys'], r['agreement_id'])).fetchall()]
                revoked = r['status'] == 'revoked'
                out.append({'agreement_id': str(r['agreement_id']), 'miner_company': f['miner_company'],
                            'hotkeys': f['hotkeys'], 'endpoints': f['endpoints'],
                            'dc_countries': sorted({d['country'] for d in f['dc_locations']}),
                            'status': 'verified', 'verified_at': iso(r['verified_at']), 'revoked': revoked,
                            'hotkey_conflicts': sorted(conflicts),
                            'routing_eligible': not revoked})
        return out
