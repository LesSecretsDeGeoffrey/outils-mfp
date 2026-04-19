"""
Build per-category mini-PDFs from recettes-geoffrey.json.

Each biscuit family (madeleines, financiers, brownies...), each pâte à tarte
family, crème family, etc gets its own dark & gold PDF. Source : the same
JSON that feeds the main fondations book — recipes are identical, just
repackaged one family per fichier.

Run : python3 scripts/build_category_pdfs.py
Output : /Users/geoffrey/Documents/Claude/PDF RESSOURCES/REFAITS/par-categorie/
"""
import os
import sys
import json

from reportlab.platypus import Spacer, PageBreak, Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from branded_pdf import (  # noqa: E402
    styles, gold_line, section_heading, recipe_card, pretty_ing,
    build_pdf, gold_callout,
)

ROOT = os.path.abspath(os.path.join(HERE, '..'))
JSON_PATH = os.path.join(ROOT, 'data', 'recettes-geoffrey.json')
OUT_DIR = '/Users/geoffrey/Documents/Claude/PDF RESSOURCES/REFAITS/par-categorie'
os.makedirs(OUT_DIR, exist_ok=True)

with open(JSON_PATH) as f:
    DATA = json.load(f)


# ──────────────────────────────────────────────────────────────
# CATEGORY DEFINITIONS
# Each category : id (for file name), titre, soustitre, famille (for
# running header), section path in JSON, ordered keys, optional intro text.
# Intro appears between cover and recipes. If multiple recipes, TOC is also
# generated. For single-recipe categories, a simpler layout is used.
# ──────────────────────────────────────────────────────────────

# Shared blurbs (keep short — under 2 sentences for compact PDFs)
BISCUITS_INTRO = (
    "Même moule, mêmes grammages, variations nature / cacao / praliné. "
    "Choisis ta version selon ton entremets, garde le process au gramme près."
)

CATEGORIES = [
    # ── BISCUITS ──────────────────────────────────────────────
    {
        'id': '01-madeleines', 'section': 'biscuits',
        'titre': 'Madeleines',
        'soustitre': "Nature, cacao, praliné — même moule, trois saveurs",
        'famille': 'Biscuits · Madeleines',
        'keys': ['madeleine', 'madeleine-cacao', 'madeleine-praline'],
        'intro': BISCUITS_INTRO,
        'cloture': "Astuce : bien huiler le moule, remplir aux 3/4, laisser reposer "
                   "la pâte 1 h au frigo avant cuisson pour une bosse bien marquée.",
    },
    {
        'id': '02-financiers', 'section': 'biscuits',
        'titre': 'Financiers',
        'soustitre': "Nature, cacao, praliné — beurre noisette et poudre d'amande",
        'famille': 'Biscuits · Financiers',
        'keys': ['financier', 'financier-cacao', 'financier-praline'],
        'intro': BISCUITS_INTRO,
        'cloture': "Le secret : un vrai beurre noisette (légèrement fumant, odeur "
                   "de caramel) et des moules bien huilés pour les bords croustillants.",
    },
    {
        'id': '03-brownies', 'section': 'biscuits',
        'titre': 'Brownies',
        'soustitre': "Chocolat noir, au lait, chocolat blanc — trois textures fondantes",
        'famille': 'Biscuits · Brownies',
        'keys': ['brownie', 'brownie-lait', 'brownie-blanc'],
        'intro': "Trois variantes, même méthode : chocolat fondu au bain-marie, "
                 "mélange vif, cuisson courte pour un cœur fondant.",
        'cloture': "Ne sur-cuis jamais un brownie — sors-le quand le centre tremble "
                   "encore légèrement, il finit de prendre hors du four.",
    },
    {
        'id': '04-dacquoises', 'section': 'biscuits',
        'titre': 'Dacquoises',
        'soustitre': "Nature et cacao — ta meringue aux amandes pour les entremets",
        'famille': 'Biscuits · Dacquoises',
        'keys': ['dacquoise', 'dacquoise-cacao'],
        'intro': "La dacquoise (ou succès) est une meringue française enrichie aux "
                 "poudres d'amandes. Croquante dehors, moelleuse dedans.",
        'cloture': "Pour un entremets, dresse à la poche directement sur tapis siliconé "
                   "et cuis à chaleur tournante 170 °C.",
    },
    {
        'id': '05-genoises', 'section': 'biscuits',
        'titre': 'Génoises',
        'soustitre': "Nature et cacao — la base légère des layer cakes et roulés",
        'famille': 'Biscuits · Génoises',
        'keys': ['genoise-nature', 'genoise-cacao'],
        'intro': "Génoise : œufs entiers + sucre montés au bain-marie, farine "
                 "ajoutée délicatement. Une mie fine, légère, qui boit le sirop.",
        'cloture': "Toujours imbiber la génoise d'un sirop parfumé avant garnissage — "
                   "c'est ce qui change tout entre un gâteau sec et un gâteau pâtissier.",
    },
    {
        'id': '06-biscuits-joconde', 'section': 'biscuits',
        'titre': 'Biscuits Joconde',
        'soustitre': "Nature et cacao — le biscuit fin des entremets et opéras",
        'famille': 'Biscuits · Joconde',
        'keys': ['joconde', 'joconde-cacao'],
        'intro': "Le biscuit Joconde est un classique des entremets : amandes, "
                 "œufs et blancs montés, cuisson rapide pour un biscuit moelleux et souple.",
        'cloture': "Étale à la spatule coudée sur tapis siliconé (3 mm), cuis chaleur "
                   "tournante 8-10 min. Démoule tiède pour éviter qu'il ne casse.",
    },
    {
        'id': '07-pains-de-genes', 'section': 'biscuits',
        'titre': 'Pains de Gênes',
        'soustitre': "Nature et cacao — 50% de pâte d'amandes, mie serrée et parfumée",
        'famille': 'Biscuits · Pain de Gênes',
        'keys': ['pain-de-genes', 'pain-de-genes-cacao'],
        'intro': "Le pain de Gênes est bâti autour d'une pâte d'amandes de qualité. "
                 "Mie serrée, parfum intense d'amande, idéal comme insert ou base.",
        'cloture': "Utilise une pâte d'amandes 50% minimum. Cuis en cadre ou en moule "
                   "haut pour un biscuit épais qui ne s'effondre pas.",
    },
    {
        'id': '08-biscuits-pate-choux', 'section': 'biscuits',
        'titre': 'Biscuits Pâte à Choux',
        'soustitre': "Japonais et cacao — la pâte à choux transformée en biscuit moelleux",
        'famille': 'Biscuits · Pâte à Choux',
        'keys': ['pate-a-choux-japonais', 'pate-a-choux-cacao'],
        'intro': "Variante hybride : pâte à choux allégée en beurre, enrichie en jaunes "
                 "et blancs montés. Un biscuit souple, moelleux, proche du Joconde.",
        'cloture': "Garde une cuisson basse et longue pour un séchage homogène sans "
                   "croûte trop craquante — ce biscuit doit rester souple.",
    },
    {
        'id': '09-biscuits-sacher', 'section': 'biscuits',
        'titre': 'Biscuits Sacher',
        'soustitre': "Nature et cacao — moelleux, chocolaté, parfait pour les entremets chocolat",
        'famille': 'Biscuits · Sacher',
        'keys': ['sacher', 'sacher-cacao'],
        'intro': "Le biscuit Sacher est l'âme des grands entremets chocolat : "
                 "pâte d'amandes, beurre, chocolat noir, blancs montés. Dense mais moelleux.",
        'cloture': "Imbibe d'un sirop au kirsch ou au rhum avant montage — c'est la "
                   "tradition viennoise, et ça booste l'intensité.",
    },
    {
        'id': '10-biscuits-savoie', 'section': 'biscuits',
        'titre': 'Biscuits de Savoie',
        'soustitre': "Nature et cacao — aérien, léger comme l'air, moule cannelé",
        'famille': 'Biscuits · Savoie',
        'keys': ['savoie', 'savoie-cacao'],
        'intro': "Le Savoie est un biscuit hyper aérien basé sur des blancs montés "
                 "très fermes et une farine légère. Idéal pour un dessert frais.",
        'cloture': "Ne cogne pas le moule en le tapotant — la structure repose sur "
                   "les bulles des blancs. Dépose délicatement la pâte et cuis doucement.",
    },
    {
        'id': '11-biscuits-trocadero', 'section': 'biscuits',
        'titre': 'Biscuits Trocadéro',
        'soustitre': "Nature et cacao — moelleux, noisette, la base des petits gâteaux individuels",
        'famille': 'Biscuits · Trocadéro',
        'keys': ['trocadero', 'trocadero-cacao'],
        'intro': "Le Trocadéro : cousin du financier, plus moelleux, bâti autour "
                 "de la poudre de noisette et de blancs non montés. Texture pâte souple.",
        'cloture': "Pour un contraste de textures, ajoute quelques pépites de chocolat "
                   "ou des éclats de praliné avant cuisson.",
    },
    {
        'id': '12-biscuits-viennois', 'section': 'biscuits',
        'titre': 'Biscuits Viennois',
        'soustitre': "Nature et cacao — souple, roulable, parfait pour les bûches",
        'famille': 'Biscuits · Viennois',
        'keys': ['viennois', 'viennois-cacao'],
        'intro': "Le biscuit Viennois est souple et roulable à chaud — le biscuit "
                 "de référence pour les bûches, roulés et gâteaux renversés.",
        'cloture': "Démoule tiède sur un torchon humide, roule tout de suite dans le "
                   "torchon. Tu pourras dérouler plus tard sans casser.",
    },

    # ── PÂTES À TARTE ─────────────────────────────────────────
    {
        'id': '13-pates-sablees', 'section': 'pates-a-tarte',
        'titre': 'Pâtes Sablées',
        'soustitre': "Nature et cacao — la plus friable, sable fin des tartes",
        'famille': 'Pâtes à tarte · Sablées',
        'keys': ['pate-sablee', 'pate-sablee-cacao'],
        'intro': "Technique du sablage : beurre froid + farine travaillés jusqu'à "
                 "obtenir un sable fin, puis liaison rapide. Texture friable, fond de tarte.",
        'cloture': "Ne jamais corser la pâte : dès qu'elle est homogène, stop. "
                   "Repos 2 h minimum, abaisse directement sortie du frigo pour bien travailler.",
    },
    {
        'id': '14-pates-sucrees', 'section': 'pates-a-tarte',
        'titre': 'Pâtes Sucrées',
        'soustitre': "Nature et cacao — technique du crémage, plus croustillante que sablée",
        'famille': 'Pâtes à tarte · Sucrées',
        'keys': ['pate-sucree', 'pate-sucree-cacao'],
        'intro': "Crémage : beurre pommade + sucre glace monté, puis œuf et farine. "
                 "Une pâte plus fine, plus sablée, moins friable — idéale pour petits fours.",
        'cloture': "Abaisse entre deux feuilles de papier cuisson pour éviter de rajouter "
                   "de la farine. Congèle tes fonds abaissés pour cuisson à froid : "
                   "résultat net, zéro déformation.",
    },
    {
        'id': '15-sables-bretons', 'section': 'pates-a-tarte',
        'titre': 'Sablés Bretons',
        'soustitre': "Nature et cacao — beurré, sablé épais, base d'entremets individuels",
        'famille': 'Pâtes à tarte · Sablés Bretons',
        'keys': ['sable-breton', 'sable-breton-cacao'],
        'intro': "Le Sablé Breton : 50% de beurre, jaunes, levure chimique. "
                 "Une pâte dense, très beurrée, que l'on cuit épaisse (8-10 mm).",
        'cloture': "Cuis dans un cercle beurré pour obtenir un disque net. "
                   "Base parfaite pour entremets individuels et tartes croustillantes.",
    },

    # ── PÂTE À CHOUX ──────────────────────────────────────────
    {
        'id': '16-pate-a-choux', 'section': 'pate-a-choux',
        'titre': 'Pâte à Choux',
        'soustitre': "Nature, chocolat, craquelins et dorure — la famille complète",
        'famille': 'Pâte à choux',
        'keys': ['pate-a-choux', 'pate-a-choux-chocolat',
                 'craquelin', 'craquelin-cacao', 'dorure-chou'],
        'intro': "Le panel complet pour réussir choux, éclairs, religieuses, Paris-Brest. "
                 "Pâte à choux classique et chocolatée, deux craquelins, dorure Mycryo.",
        'cloture': "Cuis toujours à chaleur statique 170-180 °C, porte fermée jusqu'à "
                   "coloration. Un chou ouvert à mi-cuisson retombe. Patience.",
    },

    # ── MACARONS ──────────────────────────────────────────────
    {
        'id': '17-coques-macarons', 'section': 'macarons',
        'titre': 'Coques Macarons',
        'soustitre': "Meringue française et italienne, nature et cacao — pour 35 coques",
        'famille': 'Macarons · Coques',
        'keys': ['meringue-francaise-35', 'meringue-francaise-35-cacao',
                 'meringue-italienne-35', 'meringue-italienne-35-cacao'],
        'intro': "Deux méthodes, deux écoles : la française (simple et rapide) "
                 "et l'italienne (régulière, idéale pour volume). À toi de choisir.",
        'cloture': "Croûtage indispensable pour les deux méthodes. Cuis chaleur tournante "
                   "145-150 °C, 13-15 min. Si tes coques craquent → four trop chaud.",
    },

    # ── CRÈMES ────────────────────────────────────────────────
    {
        'id': '18-cremes-patissieres', 'section': 'cremes-garnitures',
        'titre': 'Crèmes Pâtissières',
        'soustitre': "Vanille, chocolat, praliné, fruits, infusée — cinq déclinaisons",
        'famille': 'Crèmes · Pâtissières',
        'keys': ['creme-patissiere-vanille', 'creme-patissiere-chocolat',
                 'creme-patissiere-praline', 'creme-patissiere-fruits',
                 'creme-patissiere-infusee'],
        'intro': "Même technique de base (lait bouilli, jaunes + sucre + poudre à crème, "
                 "ébullition finale), cinq variations de parfum. La base de toutes les crèmes.",
        'cloture': "Filme toujours au contact dès la cuisson terminée. 24 h au frigo "
                   "avant utilisation — c'est là qu'elle prend vraiment son goût.",
    },
    {
        'id': '19-cremes-mousselines', 'section': 'cremes-garnitures',
        'titre': 'Crèmes Mousselines',
        'soustitre': "Pâtissière + beurre — cinq parfums pour garnir choux et Paris-Brest",
        'famille': 'Crèmes · Mousselines',
        'keys': ['creme-mousseline-vanille', 'creme-mousseline-chocolat',
                 'creme-mousseline-praline', 'creme-mousseline-fruits',
                 'creme-mousseline-infusee'],
        'intro': "Mousseline = pâtissière + beurre. La crème des grands classiques "
                 "(Paris-Brest, fraisier, mille-feuille). Riche, aérée, tenue parfaite.",
        'cloture': "Les deux matières à la même température (21 °C) avant montage. "
                   "Sinon la mousseline tranche. Monte au fouet 5 min pour l'aérer.",
    },
    {
        'id': '20-cremes-diplomates', 'section': 'cremes-garnitures',
        'titre': 'Crèmes Diplomates',
        'soustitre': "Pâtissière + gélatine + crème montée — cinq parfums aériens",
        'famille': 'Crèmes · Diplomates',
        'keys': ['creme-diplomate-vanille', 'creme-diplomate-chocolat',
                 'creme-diplomate-praline', 'creme-diplomate-fruits',
                 'creme-diplomate-infusee'],
        'intro': "Diplomate = pâtissière + gélatine + crème fouettée. Une texture "
                 "mousse, plus légère que mousseline, se tient grâce à la gélatine.",
        'cloture': "Incorpore la crème fouettée en 2-3 fois à la maryse, doucement, "
                   "sans casser les bulles. Utilise dans les 6 h après montage.",
    },
    {
        'id': '21-cremeux', 'section': 'cremes-garnitures',
        'titre': 'Crémeux',
        'soustitre': "Chocolat noir, lait, blanc, praliné, fruits, infusé — six textures fondantes",
        'famille': 'Crèmes · Crémeux',
        'keys': ['cremeux-chocolat-noir', 'cremeux-chocolat-lait',
                 'cremeux-chocolat-blanc', 'cremeux-chocolat-blanc-praline',
                 'cremeux-chocolat-blanc-fruits', 'cremeux-chocolat-blanc-infuse'],
        'intro': "Crémeux = crème anglaise + chocolat + gélatine éventuelle. "
                 "Texture intermédiaire entre ganache et mousse, fondant, crémeux.",
        'cloture': "Cuis ta crème anglaise à 83 °C max (nappe la cuillère sans bouillir). "
                   "Mixe 2 min au plongeant pour un crémeux bien lisse.",
    },
    {
        'id': '22-namelakas', 'section': 'cremes-garnitures',
        'titre': 'Namelakas',
        'soustitre': "Chocolat noir, lait, Dulcey, blanc, praliné, fruits, infusée — sept textures soyeuses",
        'famille': 'Crèmes · Namelakas',
        'keys': ['namelaka-chocolat-noir', 'namelaka-chocolat-lait',
                 'namelaka-chocolat-dulcey', 'namelaka-chocolat-blanc',
                 'namelaka-pralinee', 'namelaka-fruits', 'namelaka-infusee'],
        'intro': "La namelaka (japonais = onctueux) : chocolat + lait chaud + gélatine "
                 "+ crème froide. Une texture unique, soyeuse, qui se poche à merveille.",
        'cloture': "Laisse reposer 24 h au frigo avant pochage. Plus elle mûrit, plus "
                   "elle devient onctueuse et tient parfaitement la pression de la douille.",
    },
    {
        'id': '23-ganaches-cremes', 'section': 'cremes-garnitures',
        'titre': 'Ganaches de garniture',
        'soustitre': "Classiques et montées — les 14 ganaches de base par chocolat",
        'famille': 'Crèmes · Ganaches',
        'keys': ['ganache-chocolat-noir', 'ganache-chocolat-lait',
                 'ganache-chocolat-blanc', 'ganache-praline',
                 'ganache-chocolat-noir-fruits', 'ganache-chocolat-blanc-fruits',
                 'ganache-infusee',
                 'ganache-montee-chocolat-noir', 'ganache-montee-chocolat-lait',
                 'ganache-montee-chocolat-blanc', 'ganache-montee-dulcey',
                 'ganache-montee-pralinee', 'ganache-montee-chocolat-blanc-fruits',
                 'ganache-montee-infusee'],
        'intro': "Les ganaches de base, classiques et montées, par type de chocolat. "
                 "Pour les déclinaisons aromatiques (yuzu, jasmin, café…), vois le Guide ultime.",
        'cloture': "Règle universelle : émulsion au centre en 3 fois, mixage plongeant "
                   "à la fin, cristallisation 12 h minimum filmée au contact.",
    },
    {
        'id': '24-confits-praline', 'section': 'cremes-garnitures',
        'titre': 'Confits et Praliné',
        'soustitre': "Confits de fruits et praliné maison — les inserts qui font la différence",
        'famille': 'Crèmes · Inserts',
        'keys': ['confit-de-fruits', 'confit-de-fruits-aromatise', 'praline'],
        'intro': "Les inserts qui boostent tes entremets : confit de fruits pour "
                 "l'acidité et le punch, praliné maison pour la gourmandise pure.",
        'cloture': "Un praliné bien torréfié change tout. Cuis tes fruits secs au "
                   "four à 160 °C 15 min avant de caraméliser — parfum décuplé.",
    },
]


# ──────────────────────────────────────────────────────────────
# Import the private helpers from build_all_pdfs.py for consistency
# ──────────────────────────────────────────────────────────────

# We copy-re-use the meta / notes helpers used in the main fondations book so
# each category card looks identical to the one in Le livre de bord.

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
    if r.get('conservation-jours'):
        bits.append(f"Conservation {r['conservation-jours']} j")
    return bits or None


_creme_meta = _pate_meta  # same fields


def _build_usages_note(r):
    parts = []
    if r.get('usages'):
        u = r['usages']
        if isinstance(u, list):
            parts.append("Usages : " + ", ".join(u))
    if r.get('conservation'):
        parts.append(f"Conservation : {r['conservation']}")
    return '. '.join(parts) if parts else None


# ──────────────────────────────────────────────────────────────
# META FUNCTION PER SECTION
# ──────────────────────────────────────────────────────────────

META_BY_SECTION = {
    'biscuits': (_biscuit_meta, True),      # include format-reference
    'pates-a-tarte': (_pate_meta, False),
    'pate-a-choux': (None, False),
    'macarons': (None, False),
    'cremes-garnitures': (_creme_meta, False),
}


# ──────────────────────────────────────────────────────────────
# CATEGORY RENDERER
# ──────────────────────────────────────────────────────────────

def build_category(cat):
    """Return a content_fn for build_pdf()."""
    section_data = DATA.get(cat['section'], {})
    keys = cat['keys']
    recipes = [(k, section_data[k]) for k in keys if k in section_data
               and isinstance(section_data[k], dict)]
    missing = [k for k in keys if k not in section_data]
    if missing:
        print(f"  [warning] {cat['id']} missing keys: {missing}")

    meta_fn, include_format = META_BY_SECTION.get(cat['section'], (None, False))

    def _content(story):
        s = styles()

        # Intro
        if cat.get('intro'):
            story.append(Spacer(1, 10))
            story.append(Paragraph(cat['titre'], s['h2']))
            story.append(gold_line(0.4, 2, 10))
            story.append(Paragraph(cat['intro'], s['body']))
            story.append(Spacer(1, 14))

        # TOC only if more than 2 recipes
        if len(recipes) > 2:
            story.append(Paragraph('§ Dans ce guide', s['h3']))
            story.append(gold_line(0.3, 2, 6))
            for key, r in recipes:
                nom = r.get('nom', pretty_ing(key))
                total = r.get('total')
                meta_bits = []
                if total:
                    meta_bits.append(f"{total} g")
                meta_str = f" · {' · '.join(meta_bits)}" if meta_bits else ''
                story.append(Paragraph(
                    f'<link href="#recipe-{key}" color="#C8A04A">'
                    f'→ {nom}</link>'
                    f'<font color="#8A7D72" size="8">{meta_str}</font>',
                    s['body']
                ))
            story.append(Spacer(1, 4))

        # Recipe cards, one per page
        for key, r in recipes:
            story.append(PageBreak())
            kwargs = {
                'anchor': f'recipe-{key}',
                'total': r.get('total'),
                'rendement': r.get('rendement'),
                'ingredients': r.get('ingredients'),
                'cuisson': r.get('cuisson'),
                'preparation': r.get('preparation'),
                'description': r.get('description'),
            }
            if include_format:
                kwargs['format_reference'] = r.get('format-reference')
            notes = r.get('notes')
            if not notes:
                notes = _build_usages_note(r)
            kwargs['notes'] = notes
            if meta_fn:
                kwargs['meta_extras'] = meta_fn(r)
            story.extend(recipe_card(r.get('nom', pretty_ing(key)), **kwargs))

        # Closing callout
        if cat.get('cloture'):
            story.append(PageBreak())
            story.append(Spacer(1, 80))
            story.append(gold_callout(
                "Garde ça en tête",
                cat['cloture']
            ))

    return _content


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    for cat in CATEGORIES:
        filename = f"{cat['id']} - {cat['titre']}.pdf"
        out_path = os.path.join(OUT_DIR, filename)
        build_pdf(
            out_path,
            title=cat['titre'],
            subtitle=cat['soustitre'],
            running_header=cat['titre'],
            overline_text=f"MÉTHODE FONDATIONS PRO  ·  {cat['famille']}",
            tagline="— Geoffrey —",
            content_fn=build_category(cat),
        )
        size_kb = os.path.getsize(out_path) // 1024
        print(f"  ✓ {filename}  ({size_kb} KB)")


if __name__ == '__main__':
    main()
