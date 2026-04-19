"""
Branded PDF library — Les Secrets De Geoffrey (Dark & Gold)
Design system :
  - Dark    #1A1410
  - Cream   #FDF8F0
  - Gold    #C8A04A
  - Serif titres (Times), Sans corps (Helvetica), Mono badges (Courier)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak, Image, FrameBreak
)

# ── BRAND PALETTE ──
DARK      = HexColor('#1A1410')
CREAM     = HexColor('#FDF8F0')
GOLD      = HexColor('#C8A04A')
GOLD_SOFT = HexColor('#E4C584')
TEXT      = HexColor('#1A1410')
TEXT_MUTED= HexColor('#6B5E4F')
LINE_SOFT = HexColor('#D4C7B5')
WHITE     = HexColor('#FFFFFF')

LOGO_LOCAL = "/Users/geoffrey/Documents/Claude/logos/logo-principal.png"


# ── STYLES ──
def styles():
    return {
        'cover_overline': ParagraphStyle(
            'CovOver', fontName='Courier-Bold', fontSize=9, textColor=GOLD,
            alignment=TA_CENTER, spaceAfter=16, leading=12),
        'cover_title': ParagraphStyle(
            'CovTitle', fontName='Times-Roman', fontSize=38, textColor=CREAM,
            alignment=TA_CENTER, leading=44, spaceAfter=12),
        'cover_sub': ParagraphStyle(
            'CovSub', fontName='Helvetica', fontSize=13, textColor=HexColor('#BFB5A8'),
            alignment=TA_CENTER, leading=18, spaceAfter=30),
        'cover_brand': ParagraphStyle(
            'CovBrand', fontName='Times-Italic', fontSize=13, textColor=GOLD,
            alignment=TA_CENTER, leading=16),

        'h1': ParagraphStyle(
            'H1', fontName='Times-Roman', fontSize=26, textColor=DARK,
            alignment=TA_LEFT, leading=30, spaceBefore=6, spaceAfter=10),
        'h2': ParagraphStyle(
            'H2', fontName='Times-Roman', fontSize=20, textColor=DARK,
            alignment=TA_LEFT, leading=24, spaceBefore=20, spaceAfter=8),
        'h3': ParagraphStyle(
            'H3', fontName='Times-Bold', fontSize=14, textColor=DARK,
            alignment=TA_LEFT, leading=18, spaceBefore=12, spaceAfter=6),
        'overline': ParagraphStyle(
            'Over', fontName='Courier-Bold', fontSize=8, textColor=GOLD,
            alignment=TA_LEFT, leading=10, spaceAfter=4),
        'body': ParagraphStyle(
            'Body', fontName='Helvetica', fontSize=10, textColor=TEXT,
            leading=14, spaceAfter=5, alignment=TA_LEFT),
        'body_italic': ParagraphStyle(
            'BodyIt', fontName='Helvetica-Oblique', fontSize=10, textColor=TEXT_MUTED,
            leading=14, spaceAfter=5),
        'body_small': ParagraphStyle(
            'Small', fontName='Helvetica', fontSize=9, textColor=TEXT_MUTED,
            leading=12, spaceAfter=4),
        'bullet': ParagraphStyle(
            'Bul', fontName='Helvetica', fontSize=10, textColor=TEXT,
            leading=14, spaceAfter=3, leftIndent=14, bulletIndent=2),
        'quote': ParagraphStyle(
            'Quote', fontName='Times-Italic', fontSize=11, textColor=DARK,
            leading=16, spaceAfter=8, leftIndent=14, alignment=TA_LEFT),
        'card_title': ParagraphStyle(
            'CardT', fontName='Times-Bold', fontSize=13, textColor=DARK,
            leading=16, spaceAfter=4),
        'card_meta': ParagraphStyle(
            'CardM', fontName='Courier-Bold', fontSize=8, textColor=GOLD,
            leading=11, spaceAfter=4),
        'ing_label': ParagraphStyle(
            'Ing', fontName='Helvetica', fontSize=9.5, textColor=TEXT, leading=12),
        'ing_value': ParagraphStyle(
            'IngV', fontName='Helvetica-Bold', fontSize=9.5, textColor=DARK,
            leading=12, alignment=TA_RIGHT),
        'step_num': ParagraphStyle(
            'SN', fontName='Times-Bold', fontSize=11, textColor=GOLD,
            alignment=TA_CENTER, leading=14),
        'step_text': ParagraphStyle(
            'ST', fontName='Helvetica', fontSize=10, textColor=TEXT,
            leading=14, spaceAfter=2),
        'note_gold': ParagraphStyle(
            'NG', fontName='Helvetica-Oblique', fontSize=9.5, textColor=DARK,
            leading=13, spaceAfter=4, leftIndent=10),
        'footer': ParagraphStyle(
            'F', fontName='Courier-Bold', fontSize=7, textColor=GOLD,
            alignment=TA_CENTER, leading=10),
        'chapter_badge': ParagraphStyle(
            'Chap', fontName='Courier-Bold', fontSize=9, textColor=GOLD,
            alignment=TA_LEFT, leading=12, spaceAfter=4),
    }


# ── LAYOUT HELPERS ──

def gold_line(thick=0.6, before=6, after=6):
    return HRFlowable(width="100%", thickness=thick, color=GOLD,
                      spaceBefore=before, spaceAfter=after)

def section_heading(text, subtitle=None):
    s = styles()
    els = []
    els.append(Paragraph(f'<font color="#C8A04A">§</font> <b>{text}</b>', s['h2']))
    if subtitle:
        els.append(Paragraph(subtitle, s['body_italic']))
    els.append(gold_line(0.6, 4, 12))
    return els


def overline(text):
    return Paragraph(text.upper(), styles()['overline'])


_ACCENT_FIX = {
    'creme': 'crème', 'cremes': 'crèmes',
    'detrempe': 'détrempe',
    'beurre manie': 'beurre manié', 'manie': 'manié',
    'carre': 'carré', 'carres': 'carrés',
    'gelatine': 'gélatine',
    'puree': 'purée', 'purees': 'purées',
    'ble': 'blé',
    'amere': 'amère',
    'grilles': 'grillés', 'grille': 'grillé',
    'caramelises': 'caramélisés',
    'chataigne': 'châtaigne',
    'pate': 'pâte', 'pates': 'pâtes',
    'pate a choux': 'pâte à choux',
    'torrefaction': 'torréfaction',
    'torrefies': 'torréfiés',
    'meringue francaise': 'meringue française',
    'sirop sucre': 'sirop de sucre',
    'matiere grasse': 'matière grasse',
    'jus citron': 'jus de citron',
    'jus yuzu': 'jus de yuzu',
    'ecorce': 'écorce',
    'equivalence': 'équivalence',
    'realisation': 'réalisation',
    'temperature': 'température',
    'oeuf': 'œuf', 'oeufs': 'œufs',
    'poudre amande': 'poudre d\'amande',
    'poudre noisette': 'poudre de noisette',
    'poudre pistache': 'poudre de pistache',
    'fruits a coque': 'fruits à coque',
    'a coque': 'à coque',
    'a la': 'à la',
    'piment espelette': "piment d'Espelette",
    'fruits rouges': 'fruits rouges',
    'eau gelatine': 'eau de gélatine',
    'sucre glace': 'sucre glace',
    'sucre cassonade': 'sucre cassonade',
    'sucre semoule': 'sucre semoule',
    'beurre cacao mycryo': 'beurre cacao mycryo',
    'fruits a coque torrefies': 'fruits à coque torréfiés',
    'regle': 'règle', 'regles': 'règles',
    'epaisseurs': 'épaisseurs', 'epaisseur': 'épaisseur',
    'mille feuilles': 'mille-feuilles', 'mille feuille': 'mille-feuille',
    'saint honore': 'Saint-Honoré',
    'saint-honore': 'Saint-Honoré',
    'disque saint honore': 'disque Saint-Honoré',
    'mille feuilles galette': 'mille-feuilles ou galette',
    'conseils generaux': 'conseils généraux',
    'chataigne': 'châtaigne',
    'caraibes': 'Caraïbes',
    'cafe': 'café',
    'the': 'thé',
    'the matcha': 'thé matcha',
    'dulce de leche': 'dulce de leche',
    'cacao': 'cacao',
}

_NO_UNIT_PREFIXES = ('gousse', 'zeste', 'oeuf-unite', 'unite')
_MINUTE_KEYS = ('torrefaction-minutes', 'minutes')


def pretty_ing(key):
    """Pretty-print an ingredient key (kebab-case -> readable)."""
    if not key:
        return ''
    s = key.replace('-', ' ').strip().lower()
    # Extract trailing numeric disambiguators (x-1, x-2) and keep them as "(1)" / "(2)"
    toks = s.split()
    suffix = ''
    if toks and toks[-1].isdigit() and int(toks[-1]) < 10 and len(toks) >= 2:
        # Only treat as disambiguator if the token BEFORE it is also digits or a percent candidate
        prev = toks[-2]
        if prev.isdigit():
            suffix = f' ({toks[-1]})'
            toks.pop()
    s = ' '.join(toks)
    # Multi-word replacements first
    for bad, good in _ACCENT_FIX.items():
        if ' ' in bad:
            s = s.replace(bad, good)
    # Single-word replacements
    words = s.split()
    out = []
    for w in words:
        lw = w.lower()
        if w.isdigit():
            iv = int(w)
            # Common chocolate/crème fat %: 30, 33, 34, 35, 40, 50, 66, 70
            if 20 <= iv <= 90:
                out.append(f"{w}%")
            else:
                out.append(w)
        elif lw in _ACCENT_FIX:
            out.append(_ACCENT_FIX[lw])
        elif len(w) >= 2 and w[0] == 't' and w[1:].isdigit():
            # Flour codes : t55 -> T55
            out.append(w.upper())
        else:
            out.append(w)
    txt = ' '.join(out) + suffix
    return txt[:1].upper() + txt[1:] if txt else txt


def fmt_value(v, unit='g', key=None):
    """Format a numeric or string value. Drops 'g' for unit-less ingredients."""
    key_l = (key or '').lower()
    if any(key_l.startswith(p) for p in _NO_UNIT_PREFIXES):
        unit = ''
    if isinstance(v, (int, float)):
        if v == int(v):
            return f"{int(v)} {unit}".strip()
        return f"{v:g} {unit}".strip()
    return str(v)


def ingredients_table(ings, col_widths=None):
    """Build a compact 2-column ingredients table from a {key: value} dict."""
    s = styles()
    if not isinstance(ings, dict):
        return Paragraph(str(ings), s['body'])

    # Flatten nested dicts (e.g. pate feuilletée: detrempe/beurrage)
    is_nested = any(isinstance(v, dict) for v in ings.values())
    rows = []

    if is_nested:
        for section_name, sub in ings.items():
            rows.append([
                Paragraph(f'<b>{pretty_ing(section_name).upper()}</b>',
                          ParagraphStyle('n', fontName='Courier-Bold', fontSize=8,
                                         textColor=GOLD, leading=11)),
                ''
            ])
            if isinstance(sub, dict):
                for k, v in sub.items():
                    rows.append([
                        Paragraph(pretty_ing(k), s['ing_label']),
                        Paragraph(fmt_value(v, key=k), s['ing_value'])
                    ])
            else:
                rows.append([Paragraph(str(sub), s['ing_label']), ''])
    else:
        for k, v in ings.items():
            rows.append([
                Paragraph(pretty_ing(k), s['ing_label']),
                Paragraph(fmt_value(v, key=k), s['ing_value'])
            ])

    cw = col_widths or [110*mm, 30*mm]
    t = Table(rows, colWidths=cw)
    ts = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -2), 0.25, LINE_SOFT),
    ]
    t.setStyle(TableStyle(ts))
    return t


def method_list(steps):
    """Numbered step list."""
    s = styles()
    rows = []
    for i, step in enumerate(steps, start=1):
        rows.append([
            Paragraph(str(i), s['step_num']),
            Paragraph(step, s['step_text'])
        ])
    t = Table(rows, colWidths=[10*mm, 150*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -2), 0.25, LINE_SOFT),
    ]))
    return t


def _extract_format(cuisson, total=None, format_reference=None):
    """Derive a 'Pour Ø X cm' / 'Cadre X × Y cm' / 'Tapis X × Y cm' string.

    Priority :
    1. format_reference (explicit JSON field) — cleanest. Supports multiple
       fields simultaneously (e.g. tapis-cm + diametre-cm) joined by ' ou '.
    2. cuisson entries with cercle/cadre/moule + diametre-cm
    3. fallback on tapis + epaisseur
    """
    # 1. Explicit reference — may combine multiple formats
    if isinstance(format_reference, dict):
        parts = []
        if 'tapis-cm' in format_reference:
            parts.append(f"Tapis {format_reference['tapis-cm']} cm")
        if 'cadre-cm' in format_reference:
            parts.append(f"Cadre {format_reference['cadre-cm']} cm")
        if 'diametre-cm' in format_reference:
            parts.append(f"Ø {format_reference['diametre-cm']} cm")
        if 'nombre' in format_reference:
            parts.append(format_reference['nombre'])
        if parts:
            # Single value gets a "Pour" prefix for natural reading.
            # Multiple values are joined by "ou" without prefix.
            if len(parts) == 1:
                return f"Pour {parts[0]}"
            return ' ou '.join(parts)

    # 2. Derived from cuisson list
    if not cuisson:
        return None
    if isinstance(cuisson, list):
        for c in cuisson:
            if not isinstance(c, dict):
                continue
            support = str(c.get('support', '')).lower()
            if 'cercle' in support or 'cadre' in support or 'moule' in support:
                if 'diametre-cm' in c:
                    return f"Pour Ø {c['diametre-cm']} cm"
                if 'dimensions-cm' in c:
                    return f"Cadre {c['dimensions-cm']} cm"
        # 3. Fallback : tapis only
        for c in cuisson:
            if not isinstance(c, dict):
                continue
            if 'epaisseur-cm' in c:
                return f"Sur tapis · {c['epaisseur-cm']} cm d'épaisseur"
    elif isinstance(cuisson, dict):
        if 'diametre-cm' in cuisson:
            return f"Pour Ø {cuisson['diametre-cm']} cm"
    return None


def recipe_card(title, total=None, rendement=None, ingredients=None,
                cuisson=None, notes=None, meta_extras=None,
                preparation=None, description=None, format_reference=None,
                anchor=None):
    """A complete recipe card.

    Returns a LIST of flowables — header+description+ingredients are grouped
    in a KeepTogether (never split), while cuisson/preparation/notes can flow
    across pages when the preparation is long.

    `anchor` (str) adds a named bookmark on the title for internal PDF links.
    """
    s = styles()
    header = []
    anchor_tag = f'<a name="{anchor}"/>' if anchor else ''
    header.append(Paragraph(f'{anchor_tag}{title}', s['card_title']))

    meta_bits = []
    if total is not None:
        meta_bits.append(f"Total {total} g")
    fmt = _extract_format(cuisson, total=total, format_reference=format_reference)
    if fmt:
        meta_bits.append(fmt)
    if rendement:
        meta_bits.append(rendement)
    if meta_extras:
        meta_bits.extend(meta_extras)
    if meta_bits:
        header.append(Paragraph("  ·  ".join(meta_bits), s['card_meta']))
    header.append(gold_line(0.4, 2, 6))

    if description:
        header.append(Paragraph(description, s['body_italic']))
        header.append(Spacer(1, 6))

    if ingredients:
        header.append(overline("Ingrédients"))
        header.append(ingredients_table(ingredients))
        header.append(Spacer(1, 6))

    body = []

    if cuisson:
        body.append(overline("Cuisson"))
        if isinstance(cuisson, list):
            rows = []
            for c in cuisson:
                support = c.get('support', '—').replace('-', ' ')
                bits = []
                if 'epaisseur-cm' in c:
                    bits.append(f"{c['epaisseur-cm']} cm")
                if 'diametre-cm' in c:
                    bits.append(f"Ø {c['diametre-cm']} cm")
                if 'dimensions-cm' in c:
                    bits.append(f"{c['dimensions-cm']} cm")
                if c.get('temperature') is not None:
                    bits.append(f"{c['temperature']}°C")
                if c.get('minutes') is not None:
                    bits.append(f"{c['minutes']} min")
                rows.append([
                    Paragraph(support.capitalize(), s['ing_label']),
                    Paragraph(" · ".join(bits), s['ing_value'])
                ])
            t = Table(rows, colWidths=[110*mm, 50*mm])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, LINE_SOFT),
            ]))
            body.append(t)
        elif isinstance(cuisson, dict):
            for k, v in cuisson.items():
                unit = ''
                k_low = k.lower()
                if 'temperature' in k_low:
                    unit = '°C'
                elif 'minute' in k_low:
                    unit = ' min'
                if isinstance(v, (int, float)) and unit:
                    v_disp = f"{v}{unit}"
                elif unit and isinstance(v, str) and unit.strip() not in v:
                    v_disp = f"{v}{unit}"
                else:
                    v_disp = str(v)
                body.append(Paragraph(
                    f"<b>{pretty_ing(k)}</b> : {v_disp}", s['body']))
        else:
            body.append(Paragraph(str(cuisson), s['body']))
        body.append(Spacer(1, 6))

    if preparation:
        body.append(overline("Préparation"))
        if isinstance(preparation, list):
            body.append(method_list(preparation))
        else:
            body.append(Paragraph(str(preparation), s['body']))
        body.append(Spacer(1, 6))

    if notes:
        body.append(overline("Notes de Geoffrey"))
        body.append(Paragraph(notes, s['note_gold']))
        body.append(Spacer(1, 4))

    body.append(gold_line(0.3, 6, 12))

    return [KeepTogether(header), *body]


def toc_page(chapters, title='Sommaire', intro=None):
    """Build a clickable table of contents.

    chapters : list of dicts like :
      {
        'number': 1,
        'title': 'Biscuits',
        'anchor': 'chap-biscuits',
        'entries': [
          {'anchor': 'recipe-genoise-nature', 'name': 'Génoise Nature'},
          ...
        ]
      }

    Returns a list of flowables (starts with its own PageBreak).
    """
    s = styles()
    els = []
    els.append(PageBreak())
    els.append(Spacer(1, 10))
    els.append(Paragraph(
        '<font color="#C8A04A">§</font> ' + title,
        ParagraphStyle('TocTitle', fontName='Times-Roman', fontSize=28,
                       textColor=DARK, leading=34, spaceAfter=6)))
    els.append(gold_line(1.2, 2, 18))

    if intro:
        els.append(Paragraph(intro, s['body_italic']))
        els.append(Spacer(1, 12))

    chap_style = ParagraphStyle(
        'TocChap', fontName='Courier-Bold', fontSize=9, textColor=GOLD,
        leading=12, spaceBefore=14, spaceAfter=6, leftIndent=0)
    entry_style = ParagraphStyle(
        'TocEntry', fontName='Helvetica', fontSize=10.5, textColor=DARK,
        leading=16, spaceAfter=1, leftIndent=14)

    for chap in chapters:
        num = chap.get('number')
        chap_title = chap.get('title', '')
        chap_anchor = chap.get('anchor', '')
        prefix = f'CHAPITRE {num:02d}  ·  ' if num else ''
        link = (f'<link href="#{chap_anchor}">{prefix}{chap_title.upper()}</link>'
                if chap_anchor else f'{prefix}{chap_title.upper()}')
        els.append(Paragraph(link, chap_style))
        for entry in chap.get('entries', []):
            name = entry.get('name', '')
            a = entry.get('anchor', '')
            if a:
                els.append(Paragraph(
                    f'<link href="#{a}"><font color="#1A1410">→ {name}</font></link>',
                    entry_style))
            else:
                els.append(Paragraph(f'→ {name}', entry_style))

    return els


def gold_callout(title, content):
    """Dark-background callout with gold title."""
    s = styles()
    t = Table(
        [[Paragraph(f'<font color="#C8A04A"><b>{title}</b></font>',
                    ParagraphStyle('gct', fontName='Times-Bold', fontSize=12,
                                   textColor=GOLD, leading=14, spaceAfter=6)),
          ],
         [Paragraph(f'<font color="#FDF8F0">{content}</font>',
                    ParagraphStyle('gcc', fontName='Helvetica', fontSize=10,
                                   textColor=CREAM, leading=14))]],
        colWidths=[160*mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), DARK),
            ('LEFTPADDING', (0, 0), (-1, -1), 14),
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LINEABOVE', (0, 0), (-1, 0), 2, GOLD),
            ('LINEBELOW', (0, -1), (-1, -1), 2, GOLD),
        ])
    )
    return KeepTogether([t, Spacer(1, 10)])


def problem_block(problem, raisons, solutions, astuce=None):
    """Anti-raté style block: problem banner + raisons + solutions."""
    s = styles()
    banner = Table(
        [[Paragraph(f'<font color="#FDF8F0"><b>{problem}</b></font>',
                    ParagraphStyle('pb', fontName='Times-Bold', fontSize=12,
                                   textColor=CREAM, leading=15))]],
        colWidths=[160*mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), DARK),
            ('LEFTPADDING', (0, 0), (-1, -1), 14),
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LINEBEFORE', (0, 0), (0, 0), 3, GOLD),
        ])
    )

    els = [banner, Spacer(1, 4)]
    els.append(overline("Pourquoi ça rate"))
    for r in raisons:
        els.append(Paragraph(f'• {r}', s['bullet']))
    els.append(Spacer(1, 4))
    els.append(overline("Comment rattraper"))
    for sol in solutions:
        els.append(Paragraph(f'• {sol}', s['bullet']))
    if astuce:
        els.append(Spacer(1, 4))
        els.append(Paragraph(f'<font color="#C8A04A"><b>→ Astuce : </b></font>{astuce}',
                             s['note_gold']))
    els.append(gold_line(0.4, 10, 14))
    return KeepTogether(els)


# ── PAGE DECORATIONS ──

def _draw_page_frame(canvas, doc):
    """Cream background + gold margin lines + footer."""
    canvas.saveState()
    # Cream background
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Top gold rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)
    # Bottom gold rule
    canvas.line(20*mm, 14*mm, A4[0] - 20*mm, 14*mm)
    # Footer
    canvas.setFont('Courier-Bold', 7)
    canvas.setFillColor(GOLD)
    canvas.drawCentredString(A4[0]/2, 9*mm,
        f'LES SECRETS DE GEOFFREY  ·  MÉTHODE FONDATIONS PRO  ·  {doc.page:02d}')
    # Running header (set via doc attr)
    header = getattr(doc, 'running_header', '')
    if header:
        canvas.setFont('Courier-Bold', 7)
        canvas.setFillColor(GOLD)
        canvas.drawCentredString(A4[0]/2, A4[1] - 12*mm, header.upper())
    canvas.restoreState()


def _draw_cover(canvas, doc):
    """Dark background for cover page."""
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Gold corner ornaments
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1)
    L = 30*mm
    m = 18*mm
    # top-left
    canvas.line(m, A4[1] - m, m + L, A4[1] - m)
    canvas.line(m, A4[1] - m, m, A4[1] - m - L)
    # top-right
    canvas.line(A4[0] - m, A4[1] - m, A4[0] - m - L, A4[1] - m)
    canvas.line(A4[0] - m, A4[1] - m, A4[0] - m, A4[1] - m - L)
    # bot-left
    canvas.line(m, m, m + L, m)
    canvas.line(m, m, m, m + L)
    # bot-right
    canvas.line(A4[0] - m, m, A4[0] - m - L, m)
    canvas.line(A4[0] - m, m, A4[0] - m, m + L)
    # Footer
    canvas.setFont('Courier-Bold', 8)
    canvas.setFillColor(GOLD)
    canvas.drawCentredString(A4[0]/2, 28*mm,
        'LES SECRETS DE GEOFFREY')
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(HexColor('#8A7F6F'))
    canvas.drawCentredString(A4[0]/2, 22*mm,
        'lessecretsdegeoffrey.fr')
    canvas.restoreState()


# ── DOCUMENT BUILDER ──

class BrandedDoc(BaseDocTemplate):
    """Two-template doc : Cover (dark) + Content (cream)."""
    def __init__(self, filename, running_header=''):
        super().__init__(filename, pagesize=A4,
                         leftMargin=22*mm, rightMargin=22*mm,
                         topMargin=24*mm, bottomMargin=22*mm,
                         title=running_header)
        self.running_header = running_header
        frame_cover = Frame(
            0, 0, A4[0], A4[1],
            leftPadding=22*mm, rightPadding=22*mm,
            topPadding=55*mm, bottomPadding=40*mm,
            showBoundary=0, id='cover')
        frame_content = Frame(
            22*mm, 22*mm,
            A4[0] - 44*mm, A4[1] - 46*mm,
            leftPadding=0, rightPadding=0,
            topPadding=4*mm, bottomPadding=4*mm,
            showBoundary=0, id='content')

        self.addPageTemplates([
            PageTemplate(id='Cover', frames=[frame_cover], onPage=_draw_cover),
            PageTemplate(id='Content', frames=[frame_content], onPage=_draw_page_frame),
        ])


def build_cover_story(title, subtitle, overline_text=None, tagline=None):
    """Story for the cover page (dark background)."""
    s = styles()
    els = []
    # Push down a bit
    els.append(Spacer(1, 40))
    if overline_text:
        els.append(Paragraph(overline_text, s['cover_overline']))
    els.append(Paragraph(title, s['cover_title']))
    # Gold divider
    els.append(Spacer(1, 4))
    els.append(HRFlowable(width=60*mm, thickness=1.5, color=GOLD,
                          hAlign='CENTER', spaceBefore=2, spaceAfter=14))
    if subtitle:
        els.append(Paragraph(subtitle, s['cover_sub']))
    if tagline:
        els.append(Spacer(1, 40))
        els.append(Paragraph(tagline, s['cover_brand']))
    return els


def build_pdf(output, title, subtitle, running_header, overline_text, tagline,
              content_fn):
    """High-level build wrapper : cover page (dark) + content pages (cream)."""
    from reportlab.platypus import NextPageTemplate, PageBreak
    doc = BrandedDoc(output, running_header=running_header)
    story = []
    # First page uses Cover template (default since it's added first)
    story.extend(build_cover_story(title, subtitle, overline_text, tagline))
    # Switch template BEFORE the page break so the break creates a Content page
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())
    # Now content on cream pages
    content_fn(story)
    doc.build(story)
    size = os.path.getsize(output) / 1024
    print(f'✓ {os.path.basename(output)}  ({size:.0f} KB)')
