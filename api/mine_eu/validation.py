"""Strict input validation. Unknown fields are rejected; every field has a maximum length."""
import ipaddress
import re
import unicodedata

EU_EEA = frozenset(
    'AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE '  # EU 27
    'IS LI NO'.split())  # EEA (non-EU)
LANGS = ('en', 'de')

SS58_RE = re.compile(r'^5[1-9A-HJ-NP-Za-km-z]{47}$')  # base58, 48 chars, starts with 5 (no checksum)
EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]{1,64}@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$")
HOST_RE = re.compile(r'^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$')
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')

LIMITS = dict(miner_company=200, miner_legal_form=100, miner_address=500, miner_register=200, miner_vat_id=50,
              signatory_name=200, signatory_role=200, signatory_email=254, privacy_contact=254, tom_statement=4000,
              provider=200, city=200, name=200, service=300, location=200)
MAX_DC, MAX_HOTKEYS, MAX_ENDPOINTS, MAX_SUBPROC = 20, 50, 20, 20

ACCEPT_FIELDS = {'lang', 'miner_company', 'miner_legal_form', 'miner_address', 'miner_country', 'miner_register',
                 'miner_vat_id', 'signatory_name', 'signatory_role', 'signatory_email', 'privacy_contact',
                 'dc_locations', 'hotkeys', 'endpoints', 'own_subprocessors', 'tom_statement'}
PREVIEW_FIELDS = ACCEPT_FIELDS | {'website'}
ACCEPT_EXTRA = {'text_sha256', 'authority_confirmed', 'terms_read', 'website'}
CONTACT_FIELDS = {'company', 'name', 'email', 'country', 'gpus', 'message', 'website'}

COUNTRY_MESSAGE = ('{field} must be an EU/EEA ISO 3166-1 alpha-2 country code (EU member states, Iceland, '
                   'Liechtenstein, Norway). Companies outside the EU/EEA cannot sign this agreement here; '
                   'please use the inquiry form instead.')


class ValidationError(Exception):
    def __init__(self, fields, message='Please correct the highlighted fields.'):
        super().__init__(message)
        self.fields = fields
        self.message = message


def _text(value, field, max_len, errors, required=True, multiline=False):
    if value is None or value == '':
        if required:
            errors[field] = 'This field is required.'
        return ''
    if not isinstance(value, str):
        errors[field] = 'Must be a string.'
        return ''
    value = value.replace('\r\n', '\n').replace('\r', '\n')
    if not multiline:
        if '\n' in value:
            errors[field] = 'Must be a single line.'
            return ''
    value = value.replace('\t', ' ').strip()
    for ch in value:
        cat = unicodedata.category(ch)
        if (cat == 'Cc' and ch != '\n') or cat in ('Cf', 'Cs', 'Co', 'Cn') or ch == ' ' or ch == ' ':
            errors[field] = 'Contains characters that are not allowed.'
            return ''
    if required and not value:
        errors[field] = 'This field is required.'
    if len(value) > max_len:
        errors[field] = f'At most {max_len} characters.'
        return ''
    return value


def _reject_unknown(data, allowed, errors):
    for key in data:
        if key not in allowed:
            errors[str(key)[:60]] = 'Unknown field.'


def _country(value, field, errors):
    if value is None or value == '':
        errors[field] = 'This field is required.'
        return ''
    if not isinstance(value, str) or value.strip().upper() not in EU_EEA:
        errors[field] = COUNTRY_MESSAGE.format(field=field)
        return ''
    return value.strip().upper()


def _email(value, field, errors, required=True):
    value = _text(value, field, LIMITS.get(field, 254), errors, required)
    if value and field not in errors and not EMAIL_RE.match(value):
        errors[field] = 'Enter a valid email address.'
    return value


def _list(value, field, max_items, errors):
    if value is None:
        return []
    if not isinstance(value, list):
        errors[field] = 'Must be a list.'
        return []
    if len(value) > max_items:
        errors[field] = f'At most {max_items} entries.'
        return []
    return value


def _valid_endpoint(ep):
    if ep.startswith('['):  # [ipv6]:port
        host, sep, port = ep[1:].partition(']:')
        if not sep:
            return False
        try:
            ipaddress.IPv6Address(host)
        except ValueError:
            return False
    else:
        host, sep, port = ep.rpartition(':')
        if not sep or not HOST_RE.match(host):
            return False
    return port.isdigit() and len(port) <= 5 and 1 <= int(port) <= 65535


def validate_agreement_fields(data):
    """Validate the fields shared by preview and accept; return normalised dict (without lang)."""
    errors = {}
    out = {}
    for f in ('miner_company', 'miner_legal_form', 'miner_address', 'miner_register',
              'signatory_name', 'signatory_role'):
        out[f] = _text(data.get(f), f, LIMITS[f], errors, True, multiline=(f == 'miner_address'))
    out['miner_address'] = re.sub(r'\s*\n\s*', ', ', out['miner_address'])
    out['miner_vat_id'] = _text(data.get('miner_vat_id'), 'miner_vat_id', LIMITS['miner_vat_id'], errors, False)
    out['miner_country'] = _country(data.get('miner_country'), 'miner_country', errors)
    out['signatory_email'] = _email(data.get('signatory_email'), 'signatory_email', errors)
    out['privacy_contact'] = _text(data.get('privacy_contact'), 'privacy_contact', LIMITS['privacy_contact'], errors)
    out['tom_statement'] = _text(data.get('tom_statement'), 'tom_statement', LIMITS['tom_statement'], errors,
                                 True, multiline=True)

    dcs = []
    raw = _list(data.get('dc_locations'), 'dc_locations', MAX_DC, errors)
    if not raw and 'dc_locations' not in errors:
        errors['dc_locations'] = 'Add at least one data-centre location.'
    for i, item in enumerate(raw):
        key = f'dc_locations[{i}]'
        if not isinstance(item, dict) or set(item) - {'provider', 'city', 'country'}:
            errors[key] = 'Each location needs provider, city and country.'
            continue
        before = len(errors)
        dcs.append({'provider': _text(item.get('provider'), key + '.provider', LIMITS['provider'], errors),
                    'city': _text(item.get('city'), key + '.city', LIMITS['city'], errors),
                    'country': _country(item.get('country'), key + '.country', errors)})
        if len(errors) > before:
            dcs.pop()
    out['dc_locations'] = dcs

    hotkeys = []
    for i, hk in enumerate(_list(data.get('hotkeys'), 'hotkeys', MAX_HOTKEYS, errors)):
        if not isinstance(hk, str) or not SS58_RE.match(hk.strip()):
            errors[f'hotkeys[{i}]'] = 'Not a valid SS58 address (48 base58 characters, starts with 5).'
        elif hk.strip() not in hotkeys:
            hotkeys.append(hk.strip())
    out['hotkeys'] = hotkeys

    endpoints = []
    for i, ep in enumerate(_list(data.get('endpoints'), 'endpoints', MAX_ENDPOINTS, errors)):
        if not isinstance(ep, str) or not _valid_endpoint(ep.strip()):
            errors[f'endpoints[{i}]'] = 'Use host:port (hostname, IPv4 or [IPv6]:port).'
        elif ep.strip() not in endpoints:
            endpoints.append(ep.strip())
    out['endpoints'] = endpoints

    subs = []
    for i, item in enumerate(_list(data.get('own_subprocessors'), 'own_subprocessors', MAX_SUBPROC, errors)):
        key = f'own_subprocessors[{i}]'
        if not isinstance(item, dict) or set(item) - {'name', 'service', 'location'}:
            errors[key] = 'Each sub-processor needs name, service and location.'
            continue
        before = len(errors)
        subs.append({'name': _text(item.get('name'), key + '.name', LIMITS['name'], errors),
                     'service': _text(item.get('service'), key + '.service', LIMITS['service'], errors),
                     'location': _text(item.get('location'), key + '.location', LIMITS['location'], errors)})
        if len(errors) > before:
            subs.pop()
    out['own_subprocessors'] = subs
    if errors:
        raise ValidationError(errors)
    return out


def validate_preview(data):
    if not isinstance(data, dict):
        raise ValidationError({'_': 'Body must be a JSON object.'})
    errors = {}
    _reject_unknown(data, PREVIEW_FIELDS, errors)
    if errors:
        raise ValidationError(errors)
    if data.get('website'):
        raise ValidationError({'website': 'Rejected.'}, 'Request rejected.')
    lang = data.get('lang', 'en')
    if lang not in LANGS:
        raise ValidationError({'lang': 'Must be "en" or "de".'})
    return lang, validate_agreement_fields(data)


def validate_accept(data):
    if not isinstance(data, dict):
        raise ValidationError({'_': 'Body must be a JSON object.'})
    errors = {}
    _reject_unknown(data, ACCEPT_FIELDS | ACCEPT_EXTRA, errors)
    if errors:
        raise ValidationError(errors)
    if data.get('website'):
        raise ValidationError({'website': 'Rejected.'}, 'Request rejected.')
    lang = data.get('lang', 'en')
    if lang not in LANGS:
        raise ValidationError({'lang': 'Must be "en" or "de".'})
    fields = validate_agreement_fields({k: v for k, v in data.items() if k in ACCEPT_FIELDS})
    errors = {}
    if data.get('authority_confirmed') is not True:
        errors['authority_confirmed'] = 'You must confirm that you are authorised to bind the company.'
    if data.get('terms_read') is not True:
        errors['terms_read'] = 'You must confirm that you have read the agreement.'
    sha = data.get('text_sha256')
    if not isinstance(sha, str) or not SHA256_RE.match(sha):
        errors['text_sha256'] = 'Missing or malformed; review the agreement first.'
    if errors:
        raise ValidationError(errors)
    return lang, fields, sha


def validate_contact(data):
    if not isinstance(data, dict):
        raise ValidationError({'_': 'Body must be a JSON object.'})
    errors = {}
    _reject_unknown(data, CONTACT_FIELDS, errors)
    if errors:
        raise ValidationError(errors)
    if data.get('website'):
        raise ValidationError({'website': 'Rejected.'}, 'Request rejected.')
    out = {
        'company': _text(data.get('company'), 'company', 200, errors),
        'name': _text(data.get('name'), 'name', 200, errors),
        'email': _email(data.get('email'), 'email', errors),
        'country': _text(data.get('country'), 'country', 100, errors, False),
        'gpus': _text(data.get('gpus'), 'gpus', 300, errors, False),
        'message': _text(data.get('message'), 'message', 4000, errors, False, multiline=True),
    }
    if errors:
        raise ValidationError(errors)
    return out
