"""PDF copy of an accepted agreement (fpdf2, embedded DejaVu so umlauts render)."""
from datetime import datetime, timezone
from pathlib import Path
import re

from fpdf import FPDF

OFFER_URL = 'https://mine.decisionmodels.io/eu'
TITLES = {'en': 'Sub-processing agreement (Art. 28(4) GDPR) — EU miner',
          'de': 'Unterauftragsverarbeitungsvertrag (Art. 28 Abs. 4 DSGVO) — EU-Miner'}
LABELS = {
    'en': dict(operator='Operator (processor)', miner='Miner (sub-processor)', acceptance='Acceptance record',
               id='Agreement ID', at='Accepted at (UTC)', signatory='Signatory', ip='IP address', version='Version',
               sha='Text SHA-256', page='Page', statement=(
                   'Accepted electronically in text form (Art. 28(9) GDPR). The operator\'s acceptance is given by '
                   'its standing offer published at ' + OFFER_URL + '.')),
    'de': dict(operator='Betreiber (Auftragsverarbeiter)', miner='Miner (Unterauftragsverarbeiter)',
               acceptance='Annahmeprotokoll', id='Vereinbarungs-ID', at='Angenommen am (UTC)',
               signatory='Unterzeichner', ip='IP-Adresse', version='Version', sha='Text-SHA-256', page='Seite',
               statement=('Elektronisch in Textform angenommen (Art. 28 Abs. 9 DSGVO). Die Annahme durch den '
                          'Betreiber erfolgt durch sein unter ' + OFFER_URL + ' veröffentlichtes dauerhaftes '
                          'Angebot.')),
}


class PdfError(Exception):
    pass


def _find_font(font_dirs, name):
    for d in font_dirs:
        p = Path(d) / name
        if p.is_file():
            return str(p)
    raise PdfError(f'font {name} not found in {list(font_dirs)}')


def _inline(text):
    text = text.replace('`', '')
    text = re.sub(r'(?<!\*)\*(?!\*)([^*\n]+)(?<!\*)\*(?!\*)', r'\1', text)  # single-star emphasis
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
    return text


class _Doc(FPDF):
    def __init__(self, agreement_id, label_page):
        super().__init__(format='A4')
        self.agreement_id = agreement_id
        self.label_page = label_page

    def footer(self):
        self.set_y(-14)
        self.set_font('DejaVu', '', 7)
        self.set_text_color(90, 90, 90)
        self.cell(0, 5, f'{self.agreement_id} · {self.label_page} {self.page_no()}/{{nb}}', align='C')
        self.set_text_color(0, 0, 0)


def _runs(pdf, text, size, base_style='', lh=5):
    parts = _inline(text).split('**')
    for i, part in enumerate(parts):
        if not part:
            continue
        pdf.set_font('DejaVu', 'B' if (i % 2 == 1 or base_style == 'B') else '', size)
        pdf.write(lh, part)
    pdf.ln(lh)


def _flush_table(pdf, rows):
    rows = [r for r in rows if not all(re.fullmatch(r':?-{2,}:?', c.strip() or '--') for c in r)]
    if not rows:
        return
    width = max(len(r) for r in rows)
    rows = [r + [''] * (width - len(r)) for r in rows]
    pdf.set_font('DejaVu', '', 8.5)
    with pdf.table(text_align='LEFT', first_row_as_headings=True, line_height=4.6) as table:
        for r in rows:
            row = table.row()
            for c in r:
                row.cell(_inline(c.strip()).replace('**', ''))
    pdf.ln(2)


def _markdown(pdf, text):
    table, para = [], False
    for line in text.replace('\r', '').split('\n'):
        stripped = line.strip()
        if stripped.startswith('|'):
            table.append([c for c in stripped.strip('|').split('|')])
            continue
        if table:
            _flush_table(pdf, table)
            table = []
        pdf.set_x(pdf.l_margin)
        m = re.match(r'^(#{1,4})\s+(.*)$', stripped)
        if not stripped:
            pdf.ln(2)
        elif m:
            size = {1: 15, 2: 12.5, 3: 11, 4: 10}[len(m.group(1))]
            pdf.ln(2)
            _runs(pdf, m.group(2), size, 'B', lh=size * 0.5 + 1.5)
        elif re.match(r'^(-{3,}|\*{3,})$', stripped):
            y = pdf.get_y() + 1
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(3)
        elif re.match(r'^[-*]\s+', stripped):
            pdf.set_x(pdf.l_margin + 5)
            pdf.set_font('DejaVu', '', 9.5)
            pdf.write(5, '• ')
            _runs(pdf, re.sub(r'^[-*]\s+', '', stripped), 9.5)
        elif re.match(r'^\d+[.)]\s+', stripped):
            n, rest = re.match(r'^(\d+[.)])\s+(.*)$', stripped).groups()
            pdf.set_x(pdf.l_margin + 3)
            pdf.set_font('DejaVu', '', 9.5)
            pdf.write(5, n + ' ')
            _runs(pdf, rest, 9.5)
        elif stripped.startswith('>'):
            pdf.set_x(pdf.l_margin + 8)
            pdf.set_text_color(60, 60, 60)
            _runs(pdf, stripped.lstrip('> ').strip(), 9.5)
            pdf.set_text_color(0, 0, 0)
        else:
            _runs(pdf, stripped, 9.5)
    if table:
        _flush_table(pdf, table)


def _party(pdf, title, lines):
    pdf.set_font('DejaVu', 'B', 10)
    pdf.cell(0, 6, title, new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('DejaVu', '', 9.5)
    for line in lines:
        if line:
            pdf.multi_cell(0, 5, line, align='L', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)


def build_pdf(record, settings):
    """record: dict with agreement_id, lang, version, rendered_text, text_sha256, fields, accepted_at, client_ip."""
    lang = record['lang'] if record['lang'] in LABELS else 'en'
    lab = LABELS[lang]
    f = record['fields']
    pdf = _Doc(record['agreement_id'], lab['page'])
    pdf.set_auto_page_break(True, margin=18)
    pdf.set_margins(18, 16, 18)
    pdf.alias_nb_pages()
    pdf.add_font('DejaVu', '', _find_font(settings.font_dirs, 'DejaVuSans.ttf'))
    pdf.add_font('DejaVu', 'B', _find_font(settings.font_dirs, 'DejaVuSans-Bold.ttf'))
    pdf.set_title(TITLES[lang])
    pdf.set_author('Decision Models')
    pdf.set_creator('mine.decisionmodels.io')
    accepted = datetime.strptime(record['accepted_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    pdf.set_creation_date(accepted)
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 15)
    pdf.multi_cell(0, 7.5, TITLES[lang], align='L', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)
    _party(pdf, lab['operator'], [settings.operator_name, settings.operator_address])
    _party(pdf, lab['miner'], [
        f"{f['miner_company']} ({f['miner_legal_form']})", f"{f['miner_address']}, {f['miner_country']}",
        f"{f['miner_register']}" + (f" · {f['miner_vat_id']}" if f.get('miner_vat_id') else '')])
    pdf.ln(1)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(3)
    # The PDF carries its own title; drop the template's leading H1 so it is not repeated.
    body = re.sub(r'\A\s*#\s+[^\n]*\n', '', record['rendered_text'])
    _markdown(pdf, body)
    # Acceptance record block.
    if pdf.get_y() > pdf.h - 80:
        pdf.add_page()
    pdf.ln(5)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(3)
    pdf.set_font('DejaVu', 'B', 11)
    pdf.cell(0, 6, lab['acceptance'], new_x='LMARGIN', new_y='NEXT')
    rows = [(lab['id'], record['agreement_id']), (lab['at'], record['accepted_at']),
            (lab['signatory'], f"{f['signatory_name']}, {f['signatory_role']} <{f['signatory_email']}>"),
            (lab['ip'], record.get('client_ip') or ''), (lab['version'], record['version']),
            (lab['sha'], record['text_sha256'])]
    for k, v in rows:
        pdf.set_font('DejaVu', 'B', 8.5)
        pdf.cell(48, 5, k)
        pdf.set_font('DejaVu', '', 8.5)
        pdf.multi_cell(0, 5, str(v), align='L', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)
    pdf.set_font('DejaVu', '', 8.5)
    pdf.multi_cell(0, 4.5, lab['statement'], align='L', new_x='LMARGIN', new_y='NEXT')
    return bytes(pdf.output())
