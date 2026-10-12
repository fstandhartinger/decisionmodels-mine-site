"""Agreement templates: {{placeholder}} Markdown rendered in a single pass and hashed."""
import hashlib
import re

from . import AGREEMENT_VERSION

PLACEHOLDER_RE = re.compile(r'\{\{\s*([a-z_0-9]+)\s*\}\}')
FIELD_KEYS = ('miner_company', 'miner_legal_form', 'miner_address', 'miner_country', 'miner_register',
              'miner_vat_id', 'signatory_name', 'signatory_role', 'signatory_email', 'privacy_contact',
              'dc_locations', 'hotkeys', 'endpoints', 'own_subprocessors', 'tom_statement')
SYSTEM_KEYS = ('accepted_at', 'agreement_id', 'version', 'text_sha256')
KNOWN_KEYS = frozenset(FIELD_KEYS + SYSTEM_KEYS)

# These three cannot be part of the text the signer hashes (they do not exist yet), so the hashed
# text carries a fixed marker and the signed copy substitutes the real values.
PENDING = {'en': '[assigned on acceptance]', 'de': '[wird bei Annahme vergeben]'}
NONE_STATED = {'en': 'none stated', 'de': 'keine Angabe'}
NOT_PROVIDED = {'en': 'not provided', 'de': 'nicht angegeben'}


class TemplateError(Exception):
    pass


def load_template(legal_dir, lang):
    path = legal_dir / f'{AGREEMENT_VERSION}.{lang}.md'
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise TemplateError(f'template missing: {path.name}') from exc
    return raw.decode('utf-8'), hashlib.sha256(raw).hexdigest()


def template_placeholders(template):
    return set(PLACEHOLDER_RE.findall(template))


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _cell(value):
    # Values land inside Markdown table cells: one line, no column separators.
    return ' '.join(str(value).replace('|', '/').split())


def _inline(items, lang):
    return '; '.join(_cell(i) for i in items) if items else NONE_STATED[lang]


SAFEGUARD = {'en': 'Contract under Art. 28(4) GDPR (section 8.4)', 'de': 'Vertrag nach Art. 28 Abs. 4 DSGVO (Ziffer 8.4)'}


def field_values(fields, lang):
    """Placeholder -> text for the signer-supplied fields."""
    v = {k: _cell(fields.get(k, '')) for k in FIELD_KEYS if k not in ('tom_statement',)}
    v['miner_vat_id'] = _cell(fields.get('miner_vat_id') or NOT_PROVIDED[lang])
    v['dc_locations'] = _inline([f"{d['provider']}, {d['city']}, {d['country']}" for d in fields['dc_locations']], lang)
    v['hotkeys'] = _inline([f'`{h}`' for h in fields['hotkeys']], lang)
    v['endpoints'] = _inline([f'`{e}`' for e in fields['endpoints']], lang)
    rows = [f"| {_cell(s['name'])} | {_cell(s['service'])} | {_cell(s['location'])} | {SAFEGUARD[lang]} |"
            for s in fields['own_subprocessors']]
    v['own_subprocessors'] = '\n'.join(rows) if rows else f'| {NONE_STATED[lang]} | | | |'
    # Quoted line by line so a multi-line statement cannot inject headings or clauses.
    v['tom_statement'] = '\n'.join('> ' + line if line else '>' for line in fields['tom_statement'].split('\n'))
    return v


def substitute(template, values):
    def repl(m):
        key = m.group(1)
        if key not in values:
            raise TemplateError(f'unknown placeholder {{{{{key}}}}}')
        return values[key]
    return PLACEHOLDER_RE.sub(repl, template)


def render_for_hash(template, fields, lang):
    """The exact text the signer reviews and whose SHA-256 must be echoed back on accept."""
    values = field_values(fields, lang)
    values.update(version=AGREEMENT_VERSION, accepted_at=PENDING[lang], agreement_id=PENDING[lang],
                  text_sha256=PENDING[lang])
    return substitute(template, values)


def render_final(template, fields, lang, agreement_id, accepted_at, text_sha256):
    values = field_values(fields, lang)
    values.update(version=AGREEMENT_VERSION, accepted_at=accepted_at, agreement_id=agreement_id,
                  text_sha256=text_sha256)
    return substitute(template, values)
