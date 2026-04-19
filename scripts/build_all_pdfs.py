"""
Build all 5 rebranded PDFs (dark & gold) from recettes-geoffrey.json.
Run : python3 scripts/build_all_pdfs.py
"""
import os, sys, json
from reportlab.platypus import Spacer, PageBreak, Paragraph, NextPageTemplate

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from branded_pdf import (  # noqa: E402
    styles, gold_line, section_heading, overline,
    recipe_card, gold_callout, problem_block, method_list,
    ingredients_table, pretty_ing, fmt_value,
    build_pdf,
)

ROOT = os.path.abspath(os.path.join(HERE, '..'))
JSON_PATH = os.path.join(ROOT, 'data', 'recettes-geoffrey.json')
OUT_DIR = '/Users/geoffrey/Documents/Claude/PDF RESSOURCES/REFAITS'
os.makedirs(OUT_DIR, exist_ok=True)

with open(JSON_PATH) as f:
    DATA = json.load(f)


# ════════════════════════════════════════════════════════════
# 1) BOOK — LES FONDATIONS DU CHEF
# ════════════════════════════════════════════════════════════

def chapter_title(story, number, title, subtitle=None):
    s = styles()
    story.append(PageBreak())
    story.append(Spacer(1, 20))
    story.append(Paragraph(f'<font color="#C8A04A">CHAPITRE {number:02d}</font>',
                           styles()['overline']))
    story.append(Paragraph(title, s['h1']))
    if subtitle:
        story.append(Paragraph(subtitle, s['body_italic']))
    story.append(gold_line(1.5, 6, 18))


def build_fondations(story):
    s = styles()

    # Intro
    story.append(Spacer(1, 12))
    story.append(Paragraph('Bienvenue dans ton livre de bord', s['h2']))
    story.append(gold_line(0.4, 2, 10))
    story.append(Paragraph(
        "Ce livre regroupe les fondations techniques de ma méthode. "
        "Tu y trouveras les recettes de base avec leurs grammages exacts, "
        "les cuissons précises et mes notes pour éviter les ratés. "
        "Rien de bavard : du concret, des chiffres, et la logique derrière chaque geste.",
        s['body']))
    story.append(Spacer(1, 10))
    story.append(gold_callout(
        'La règle d\'or',
        "Lire la recette en entier, peser TOUT au gramme près, "
        "respecter les temps de repos, noter ce qui a marché. "
        "La pâtisserie ne pardonne pas l'approximation."
    ))
    story.append(Spacer(1, 6))

    # CH 01 : BISCUITS
    biscuits = DATA['biscuits']
    chapter_title(story, 1, 'Biscuits',
                  f"{len(biscuits)} recettes de base pour tous tes entremets, gâteaux et pièces de pâtisserie")
    for key, r in biscuits.items():
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            rendement=r.get('rendement'),
            ingredients=r.get('ingredients'),
            cuisson=r.get('cuisson'),
            notes=r.get('notes') or _build_usages_note(r),
            meta_extras=_biscuit_meta(r)
        ))

    # CH 02 : PÂTES À TARTE
    pates = DATA['pates-a-tarte']
    chapter_title(story, 2, 'Pâtes à tarte',
                  f"{len(pates)} pâtes sablées, sucrées et sablés bretons — ta base pour tartes, fonds et petits-fours")
    for key, r in pates.items():
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            ingredients=r.get('ingredients'),
            cuisson=r.get('cuisson'),
            notes=r.get('notes'),
            meta_extras=_pate_meta(r)
        ))

    # CH 03 : PÂTE À CHOUX
    choux = DATA['pate-a-choux']
    chapter_title(story, 3, 'Pâte à choux',
                  f"{len(choux)} recettes pour maîtriser les choux, éclairs, religieuses et Paris-Brest")
    for key, r in choux.items():
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            ingredients=r.get('ingredients'),
            cuisson=r.get('cuisson'),
            notes=r.get('notes')
        ))

    # CH 04 : MACARONS
    mac = DATA['macarons']
    chapter_title(story, 4, 'Macarons',
                  "Méthodes italienne et française à 35, avec et sans cacao")
    for key, r in mac.items():
        if key == 'astuces':
            continue
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            ingredients=r.get('ingredients'),
            cuisson=r.get('cuisson'),
            notes=r.get('notes') or r.get('procedure')
        ))
    if 'astuces' in mac:
        story.append(Spacer(1, 10))
        _render_tips(story, 'Mes astuces macarons', mac['astuces'])

    # CH 05 : PERSONNALISATION
    if 'personnalisation-biscuits' in DATA:
        perso = DATA['personnalisation-biscuits']
        chapter_title(story, 5, 'Personnaliser tes biscuits',
                      "Remplacer la farine, choisir le bon sucre — varier les textures et les saveurs")
        for section_key, content in perso.items():
            story.append(Paragraph(pretty_ing(section_key), s['h3']))
            story.append(gold_line(0.3, 2, 6))
            _render_flex(story, content)
            story.append(Spacer(1, 10))

    # CH 06 : CRÈMES & GARNITURES
    cremes = DATA['cremes-garnitures']
    chapter_title(story, 6, 'Crèmes & garnitures',
                  f"{len(cremes)} crèmes pâtissières, mousselines, diplomates, crémeux et pralinés maison")
    for key, r in cremes.items():
        meta = []
        if r.get('rendement'):
            meta.append(r['rendement'])
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            ingredients=r.get('ingredients'),
            cuisson=r.get('cuisson'),
            notes=r.get('notes'),
            meta_extras=meta or None
        ))

    # Closing
    story.append(PageBreak())
    story.append(Spacer(1, 80))
    story.append(Paragraph("Tu es maintenant armé.", styles()['h1']))
    story.append(gold_line(0.6, 6, 16))
    story.append(Paragraph(
        "Ces recettes sont les bases que j'utilise au quotidien dans la "
        "Méthode Fondations Pro. Elles sont pensées pour être testées, "
        "ajustées, combinées. Prends ton temps, teste-les une par une, "
        "prends des notes dans ton carnet, et bâtis ta propre bibliothèque.",
        styles()['body']))
    story.append(Spacer(1, 20))
    story.append(gold_callout(
        "Ce n'est qu'un début",
        "Le vrai jeu commence quand tu composes : un biscuit + une crème + un insert + une finition. "
        "C'est là que tu passes du reproducteur au créateur."
    ))


def _biscuit_meta(r):
    bits = []
    if r.get('conservation-jours'):
        bits.append(f"Conservation {r['conservation-jours']} j")
    if r.get('usages'):
        u = r['usages']
        if isinstance(u, list) and u:
            bits.append(f"Pour : {', '.join(u[:3])}{'...' if len(u) > 3 else ''}")
    return bits or None


def _pate_meta(r):
    bits = []
    if r.get('rendement'):
        bits.append(r['rendement'])
    if r.get('conservation-jours'):
        bits.append(f"Conservation {r['conservation-jours']} j")
    return bits or None


def _build_usages_note(r):
    """Compose a note from usages+conservation when no explicit note."""
    parts = []
    if r.get('usages'):
        u = r['usages']
        if isinstance(u, list):
            parts.append("Usages : " + ", ".join(u))
    if r.get('conservation'):
        parts.append(f"Conservation : {r['conservation']}")
    return '. '.join(parts) if parts else None


def _render_tips(story, title, tips):
    s = styles()
    story.append(Paragraph(title, s['h3']))
    story.append(gold_line(0.3, 2, 6))
    _render_flex(story, tips)


def _render_flex(story, content):
    """Render any dict/list/str content as paragraphs."""
    s = styles()
    if isinstance(content, dict):
        for k, v in content.items():
            if isinstance(v, (dict, list)):
                story.append(Paragraph(f'<b>{pretty_ing(k)}</b>', s['body']))
                _render_flex(story, v)
            else:
                story.append(Paragraph(f'<b>{pretty_ing(k)}</b> : {v}', s['body']))
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                _render_flex(story, item)
            else:
                story.append(Paragraph(f'• {item}', s['bullet']))
    else:
        story.append(Paragraph(str(content), s['body']))


# ════════════════════════════════════════════════════════════
# 2) GUIDE ULTIME GANACHES MONTÉES
# ════════════════════════════════════════════════════════════

def build_ganaches(story):
    s = styles()
    g = DATA['ganaches-guide']

    story.append(Spacer(1, 10))
    story.append(Paragraph('Deux familles, une technique', s['h2']))
    story.append(gold_line(0.4, 2, 10))
    story.append(Paragraph(g.get('description', ''), s['body']))
    story.append(Spacer(1, 10))

    # Méthode émulsion
    if 'methode-emulsion' in g:
        story.append(gold_callout(
            "La méthode d'émulsion",
            g['methode-emulsion']
        ))

    # Classiques
    story.append(PageBreak())
    story.append(Spacer(1, 10))
    story.extend(section_heading(
        'Ganaches classiques',
        f"{len(g.get('classiques', {}))} ganaches de fourrage et garnitures — "
        "textures fermes pour les bonbons chocolat et les pièces de pâtisserie"
    ))
    for key, r in g.get('classiques', {}).items():
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            ingredients=r.get('ingredients'),
            notes=r.get('notes')
        ))

    # Montées
    story.append(PageBreak())
    story.append(Spacer(1, 10))
    story.extend(section_heading(
        'Ganaches montées',
        f"{len(g.get('montees', {}))} ganaches aériennes — pour pocher, "
        "garnir des choux, monter des entremets légers"
    ))
    for key, r in g.get('montees', {}).items():
        story.append(recipe_card(
            r.get('nom', pretty_ing(key)),
            total=r.get('total'),
            ingredients=r.get('ingredients'),
            notes=r.get('notes')
        ))

    # Closing
    story.append(PageBreak())
    story.append(Spacer(1, 80))
    story.append(gold_callout(
        "Le principe, toujours le même",
        "Chocolat fondu + liquide chaud en 3 fois, mixage plongeant, "
        "cristallisation toute une nuit. La technique ne varie pas — "
        "seule la saveur change. Une fois maîtrisée, tu peux l'adapter "
        "à n'importe quelle infusion."
    ))


# ════════════════════════════════════════════════════════════
# 3) GUIDE ANTI-RATÉ
# ════════════════════════════════════════════════════════════

def build_anti_rate(story):
    s = styles()
    ar = DATA['anti-rate']

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        'Pourquoi ça rate, comment rattraper', s['h2']))
    story.append(gold_line(0.4, 2, 10))
    story.append(Paragraph(ar.get('description', ''), s['body']))
    story.append(Spacer(1, 10))

    # Règles d'or
    if 'regles-dor' in ar:
        rd = ar['regles-dor']
        story.append(gold_callout(
            rd.get('titre', "Les règles d'or"),
            _rules_to_html(rd.get('regles', []))
        ))

    # Catégories
    categories_order = [
        'pates-a-tarte', 'pate-a-choux', 'biscuits-cakes', 'macarons',
        'caramel', 'ganaches-cremes', 'mousses-meringues', 'entremets',
        'glacages', 'enrobages'
    ]

    for cat_key in categories_order:
        if cat_key not in ar:
            continue
        cat = ar[cat_key]
        story.append(PageBreak())
        story.append(Spacer(1, 10))
        story.extend(section_heading(cat.get('titre', pretty_ing(cat_key))))

        for p in cat.get('problemes', []):
            story.append(problem_block(
                p.get('probleme', ''),
                p.get('raisons', []),
                p.get('solutions', []),
                astuce=p.get('astuce-cle')
            ))

        # Catégorie-level astuce
        if cat.get('astuce-cle'):
            story.append(gold_callout(
                'Astuce clé',
                cat['astuce-cle']
            ))


def _rules_to_html(regles):
    """Format règles d'or list for a callout."""
    if not regles:
        return ''
    lines = []
    for r in regles:
        if isinstance(r, dict):
            num = r.get('numero') or r.get('num') or ''
            titre = r.get('nom') or r.get('titre') or ''
            desc = r.get('detail') or r.get('description') or r.get('texte') or ''
            num_prefix = f'<font color="#C8A04A">{num}. </font>' if num else ''
            if titre and desc:
                lines.append(f'{num_prefix}<b>{titre}.</b> {desc}')
            elif titre:
                lines.append(f'{num_prefix}<b>{titre}</b>')
            else:
                lines.append(desc)
        else:
            lines.append(str(r))
    return '<br/><br/>'.join(lines)


# ════════════════════════════════════════════════════════════
# 4) & 5) PÂTES FEUILLETÉES
# ════════════════════════════════════════════════════════════

def build_feuilletee(story, variant='classique'):
    s = styles()
    pf = DATA['pates-feuilletees']
    recipe = pf.get(f'feuilletee-{variant}', {})

    # Intro
    story.append(Spacer(1, 10))
    story.append(Paragraph(recipe.get('nom', ''), s['h2']))
    if recipe.get('description'):
        story.append(Paragraph(recipe['description'], s['body_italic']))
    story.append(gold_line(0.4, 6, 12))

    # Conseils généraux
    if 'conseils-generaux' in pf:
        story.append(Paragraph('Les règles du feuilletage', s['h3']))
        story.append(gold_line(0.3, 2, 6))
        _render_conseils(story, pf['conseils-generaux'])
        story.append(Spacer(1, 10))

    # Recipe card
    story.append(PageBreak())
    story.append(Spacer(1, 10))
    story.extend(section_heading('La recette', 'Grammages exacts, formes, étapes'))

    meta_extras = []
    if recipe.get('rendement'):
        meta_extras.append(f"Rendement : {recipe['rendement']}")

    # Card header
    story.append(Paragraph(recipe.get('nom', ''), styles()['card_title']))
    bits = []
    if recipe.get('total'):
        bits.append(f"Total {recipe['total']} g")
    bits.extend(meta_extras)
    if bits:
        story.append(Paragraph("  ·  ".join(bits), styles()['card_meta']))
    story.append(gold_line(0.4, 2, 8))

    # Ingrédients
    story.append(overline('Ingrédients'))
    story.append(ingredients_table(recipe.get('ingredients', {})))
    story.append(Spacer(1, 10))

    # Formes
    if recipe.get('formes'):
        story.append(overline('Formes de travail'))
        for k, v in recipe['formes'].items():
            story.append(Paragraph(_format_forme(k, v), s['body']))
        story.append(Spacer(1, 8))

    # Méthode
    if recipe.get('methode'):
        story.append(overline('La méthode, pas à pas'))
        story.append(method_list(recipe['methode']))
        story.append(Spacer(1, 10))

    # Closing with usages + conseils
    conseils = pf.get('conseils-generaux', {})
    if conseils.get('cuisson') or conseils.get('usages'):
        story.append(PageBreak())
        story.append(Spacer(1, 10))
        story.extend(section_heading('Cuisson & usages'))
        if conseils.get('cuisson'):
            story.append(Paragraph('Cuisson', s['h3']))
            story.append(Paragraph(conseils['cuisson'], s['body']))
            story.append(Spacer(1, 10))
        if conseils.get('usages'):
            story.append(Paragraph('Usages', s['h3']))
            u = conseils['usages']
            if isinstance(u, list):
                for item in u:
                    story.append(Paragraph(f'• {item}', s['bullet']))
            else:
                story.append(Paragraph(str(u), s['body']))
        story.append(Spacer(1, 20))
        story.append(gold_callout(
            'Garde ça en tête',
            "La pâte feuilletée, c'est 80% de patience et 20% de technique. "
            "Respecte les repos, garde la même température entre détrempe et beurre, "
            "et tu auras un feuilletage digne d'un pro."
        ))


def _format_forme(key, value):
    """Format a mold/forme key+value into a readable French sentence."""
    # e.g. 'detrempe-rectangle-cm' + '30 x 15'
    key_low = key.lower()
    shapes = ['rectangle', 'carre', 'carré', 'disque', 'cercle', 'ovale']
    shape = None
    for sh in shapes:
        if sh in key_low:
            shape = 'carré' if sh == 'carre' else sh
            break
    # Strip shape + 'cm' from key
    parts = [p for p in key_low.split('-')
             if p not in ('rectangle', 'carre', 'carré', 'disque', 'cercle',
                          'ovale', 'cm')]
    subject = pretty_ing('-'.join(parts))
    # Use × for dimensions
    v = value.replace('x', '×') if isinstance(value, str) else str(value)
    if shape:
        return f'<b>{subject}</b> : {shape} {v} cm'
    return f'<b>{subject}</b> : {v}'


def _render_conseils(story, conseils):
    s = styles()
    for k, v in conseils.items():
        if isinstance(v, dict):
            story.append(Paragraph(f'<b>{pretty_ing(k)}</b>', s['body']))
            for k2, v2 in v.items():
                story.append(Paragraph(f'&nbsp;&nbsp;• {pretty_ing(k2)} : {v2}', s['bullet']))
        elif isinstance(v, list):
            story.append(Paragraph(f'<b>{pretty_ing(k)}</b> : {", ".join(map(str, v))}',
                                   s['body']))
        else:
            story.append(Paragraph(f'<b>{pretty_ing(k)}</b> : {v}', s['body']))


# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

def main():
    # 1) Fondations du chef
    build_pdf(
        os.path.join(OUT_DIR, '01 - Les fondations du chef.pdf'),
        title='Les fondations du chef',
        subtitle="Recettes de base, grammages exacts et techniques maîtrisées",
        running_header='Les fondations du chef',
        overline_text='MÉTHODE FONDATIONS PRO  ·  Livre de bord',
        tagline="— Geoffrey —",
        content_fn=build_fondations
    )

    # 2) Guide ultime ganaches montées
    build_pdf(
        os.path.join(OUT_DIR, '02 - Guide ultime ganaches montees.pdf'),
        title='Guide ultime des ganaches montées',
        subtitle="Deux familles de ganaches, une méthode universelle",
        running_header='Guide ultime ganaches montées',
        overline_text='MÉTHODE FONDATIONS PRO  ·  Guide technique',
        tagline="— Geoffrey —",
        content_fn=build_ganaches
    )

    # 3) Guide anti-raté
    build_pdf(
        os.path.join(OUT_DIR, '03 - Guide anti-rate.pdf'),
        title='Guide anti-raté',
        subtitle="Pourquoi ça rate, comment rattraper, pour chaque grand classique",
        running_header='Guide anti-raté',
        overline_text='MÉTHODE FONDATIONS PRO  ·  Diagnostic',
        tagline="— Geoffrey —",
        content_fn=build_anti_rate
    )

    # 4) Pâte feuilletée classique
    build_pdf(
        os.path.join(OUT_DIR, '04 - Pate feuilletee classique.pdf'),
        title='La pâte feuilletée classique',
        subtitle="La plus croustillante — beurre enchâssé dans une détrempe",
        running_header='Pâte feuilletée classique',
        overline_text='MÉTHODE FONDATIONS PRO  ·  Technique',
        tagline="— Geoffrey —",
        content_fn=lambda s: build_feuilletee(s, 'classique')
    )

    # 5) Pâte feuilletée inversée
    build_pdf(
        os.path.join(OUT_DIR, '05 - Pate feuilletee inversee.pdf'),
        title='La pâte feuilletée inversée',
        subtitle="La plus fondante — détrempe enchâssée dans le beurre",
        running_header='Pâte feuilletée inversée',
        overline_text='MÉTHODE FONDATIONS PRO  ·  Technique',
        tagline="— Geoffrey —",
        content_fn=lambda s: build_feuilletee(s, 'inversee')
    )


if __name__ == '__main__':
    main()
