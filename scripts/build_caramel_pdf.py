"""
Build the Caramels PDF in the same dark & gold format as the other
par-categorie PDFs (18-cremes-patissieres, 21-cremeux, 22-namelakas,
23-ganaches-cremes, 24-confits-praline…).

8 variations partagent une technique commune : caramel ambré, crème chaude,
cuisson 107 °C, beurre à 70 °C, mixeur plongeant, fleur de sel.

Run : python3 scripts/build_caramel_pdf.py
Output : /Users/geoffrey/Documents/Claude/PDF RESSOURCES/REFAITS/par-categorie/25-caramel - Caramels.pdf
"""
import os
import sys
import re

from reportlab.platypus import Spacer, PageBreak, Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from branded_pdf import (  # noqa: E402
    styles, gold_line, recipe_card, build_pdf, gold_callout,
)

OUT_DIR = '/Users/geoffrey/Documents/Claude/PDF RESSOURCES/REFAITS/par-categorie'
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, '25-caramel - Caramels.pdf')


# ──────────────────────────────────────────────────────────────
# RECETTES — 8 variations partageant la même base technique
# ──────────────────────────────────────────────────────────────

CARAMELS = [
    # ── 1. Vanille (la base)
    {
        'key': 'caramel-vanille',
        'nom': 'Caramel Onctueux Vanille',
        'total': 241,
        'ingredients': {
            'sucre': 100,
            'creme': 100,
            'beurre': 40,
            'gousse-vanille': 1,
            'fleur-de-sel': 1,
        },
        'description': (
            "La base indémodable. Un caramel ambré, infusé à la vanille, "
            "terminé à la fleur de sel. L'insert signature pour entremets "
            "vanille, coulant pour bonbons chocolat, sauce pour verrines."
        ),
        'preparation': [
            "Fais infuser la vanille (graines + gousse) dans la crème pendant 30 minutes",
            "Réalise un caramel bien ambré avec le sucre",
            "Ajoute la crème bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le beurre une fois le caramel redescendu à 70 °C et mixe au mixeur plongeant",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Température cible 107 °C au thermomètre à sonde pour une texture "
            "nappante parfaite. Beurre toujours incorporé à 70 °C (plus chaud "
            "il tranche, plus froid il fige). Mixage au plongeant obligatoire "
            "pour une émulsion lisse et brillante."
        ),
        'usages': ["insert entremets vanille", "cœur coulant bonbon", "sauce verrine", "nappage tartes"],
        'conservation': "7 jours au frigo dans un pot hermétique",
    },

    # ── 2. Chocolat Noir 70%
    {
        'key': 'caramel-chocolat-noir',
        'nom': 'Caramel Chocolat Noir 70%',
        'total': 291,
        'ingredients': {
            'sucre': 100,
            'creme': 100,
            'beurre': 40,
            'chocolat-noir-70': 50,
            'fleur-de-sel': 1,
        },
        'description': (
            "Caramel corsé au chocolat noir. Intensité profonde, légère "
            "amertume qui équilibre le sucre. L'insert idéal pour entremets "
            "chocolat, bûches d'hiver, bonbons fourrés."
        ),
        'preparation': [
            "Porte la crème à frémissement",
            "Réalise un caramel bien ambré avec le sucre",
            "Ajoute la crème bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le chocolat noir haché et le beurre une fois le caramel redescendu à 70 °C",
            "Mixe au mixeur plongeant pour une émulsion parfaite",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Chocolat noir 70 % minimum pour ne pas être écrasé par le sucre "
            "du caramel. L'ajout simultané du chocolat et du beurre à 70 °C "
            "est crucial pour l'émulsion. Si la masse épaissit trop vite, "
            "rallonge de 10 g de crème chaude avant de mixer."
        ),
        'usages': ["insert entremets chocolat", "fourrage bonbon", "bûche chocolat-caramel", "tarte chocolat"],
        'conservation': "7 jours au frigo dans un pot hermétique",
    },

    # ── 3. Chocolat au Lait 40%
    {
        'key': 'caramel-chocolat-lait',
        'nom': 'Caramel Chocolat au Lait 40%',
        'total': 291,
        'ingredients': {
            'sucre': 100,
            'creme': 100,
            'beurre': 40,
            'chocolat-lait-40': 50,
            'fleur-de-sel': 1,
        },
        'description': (
            "La version la plus gourmande, parfait pour les amateurs de "
            "douceur. Le chocolat au lait amplifie le caramel et adoucit "
            "l'ensemble. Rêvé pour les entremets noisette, vanille, caramel."
        ),
        'preparation': [
            "Porte la crème à frémissement",
            "Réalise un caramel bien ambré avec le sucre (pas trop foncé, sinon ça domine le lait)",
            "Ajoute la crème bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le chocolat au lait haché et le beurre une fois le caramel redescendu à 70 °C",
            "Mixe au mixeur plongeant pour une émulsion parfaite",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Chocolat au lait 40 % minimum (Jivara Valrhona, Bahibé). "
            "Vise un caramel moins foncé qu'en version noire — ambré clair "
            "pour ne pas dominer la douceur lactée. La fleur de sel devient "
            "essentielle pour casser la sucrosité. 7 jours de conservation."
        ),
        'usages': ["entremets noisette-caramel", "insert bûche lactée", "bonbon fourré lait", "tarte lactée"],
        'conservation': "7 jours au frigo dans un pot hermétique",
    },

    # ── 4. Chocolat Blanc 35%
    {
        'key': 'caramel-chocolat-blanc',
        'nom': 'Caramel Chocolat Blanc 35%',
        'total': 281,
        'ingredients': {
            'sucre': 100,
            'creme': 80,
            'beurre': 30,
            'chocolat-blanc-35': 70,
            'fleur-de-sel': 1,
        },
        'description': (
            "Variation la plus subtile. Le chocolat blanc adoucit le caramel "
            "en conservant la note ambrée. Le ratio change : moins de crème, "
            "moins de beurre, plus de chocolat. Idéal avec fruits rouges, "
            "agrumes, fruits de la passion."
        ),
        'preparation': [
            "Porte la crème à frémissement",
            "Réalise un caramel ambré clair avec le sucre (ne pas pousser trop foncé)",
            "Ajoute la crème bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le chocolat blanc haché et le beurre une fois le caramel redescendu à 70 °C",
            "Mixe au mixeur plongeant pour une émulsion parfaite",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Ratios ajustés : chocolat blanc 70 g, crème 80 g, beurre 30 g. "
            "Le chocolat blanc apporte beaucoup de beurre de cacao, d'où la "
            "baisse de crème et de beurre pour garder l'équilibre. Caramel "
            "ambré CLAIR pour préserver la douceur. Magnifique pour insert "
            "d'entremets aux fruits rouges."
        ),
        'usages': ["entremets fraise-caramel", "insert passion", "bûche agrumes", "création signature"],
        'conservation': "7 jours au frigo dans un pot hermétique",
    },

    # ── 5. Café
    {
        'key': 'caramel-cafe',
        'nom': 'Caramel Café',
        'total': 246,
        'ingredients': {
            'sucre': 100,
            'creme': 100,
            'beurre': 40,
            'cafe-moulu': 10,
            'fleur-de-sel': 1,
        },
        'description': (
            "Infusion café dans la crème pour un caramel adulte, profond, "
            "torréfié. Fonctionne en duo avec le chocolat, la noisette ou "
            "la cacahuète. Signature de comptoir italien."
        ),
        'preparation': [
            "Porte la crème à frémissement et infuse le café moulu pendant 10 minutes hors du feu",
            "Filtre la crème au chinois très fin (ou à l'étamine) et repèse — recomplète avec de la crème si besoin pour retrouver 100 g",
            "Réalise un caramel bien ambré avec le sucre",
            "Ajoute la crème café bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le beurre une fois le caramel redescendu à 70 °C et mixe au mixeur plongeant",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Utilise du café moulu de qualité (espresso italien, grain "
            "fraîchement moulu). Alternative : 5 g d'extrait de café liquide "
            "ajouté en fin de cuisson pour une intensité contrôlée. Le café "
            "dégrade la conservation — consomme dans les 5 jours."
        ),
        'usages': ["entremets café-chocolat", "insert opéra", "bonbon café", "fourrage éclair café"],
        'conservation': "5 jours au frigo dans un pot hermétique",
    },

    # ── 6. Fruits
    {
        'key': 'caramel-fruits',
        'nom': 'Caramel aux Fruits',
        'total': 251,
        'ingredients': {
            'sucre': 100,
            'creme': 80,
            'beurre': 40,
            'puree-de-fruits': 30,
            'fleur-de-sel': 1,
        },
        'description': (
            "Caramel acidulé, frais, qui fonctionne avec purée de passion, "
            "framboise, mangue, citron, yuzu. L'acidité du fruit équilibre "
            "la sucrosité du caramel pour un insert lumineux."
        ),
        'preparation': [
            "Porte la crème à frémissement",
            "Réalise un caramel bien ambré avec le sucre",
            "Ajoute la crème bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute la purée de fruits hors du feu pour préserver la fraîcheur aromatique",
            "Ajoute le beurre une fois le caramel redescendu à 70 °C et mixe au mixeur plongeant",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Ratios ajustés : crème baissée à 80 g pour compenser l'apport "
            "liquide de la purée. Purée ajoutée HORS DU FEU à 107 °C pour "
            "préserver la fraîcheur. Fruits conseillés : passion, framboise, "
            "citron, yuzu, mangue. Évite les fruits peu acides (banane, "
            "pêche) qui ne tiennent pas face au caramel. Conservation "
            "réduite à 5 jours."
        ),
        'usages': ["insert entremets fruité", "tarte passion-caramel", "verrine mangue", "bonbon fruit-caramel"],
        'conservation': "5 jours au frigo dans un pot hermétique",
    },

    # ── 7. Praliné / Purée de fruits à coque
    {
        'key': 'caramel-praline',
        'nom': 'Caramel Praliné',
        'total': 301,
        'ingredients': {
            'sucre': 100,
            'creme': 100,
            'beurre': 40,
            'praline-amande-noisette': 60,
            'fleur-de-sel': 1,
        },
        'description': (
            "L'association double caramel + fruits à coque. Utilise du "
            "praliné amande-noisette maison ou une purée pure de noisette, "
            "d'amande, de pistache, de cacahuète. Pour les entremets "
            "gourmands à l'extrême."
        ),
        'preparation': [
            "Porte la crème à frémissement",
            "Réalise un caramel bien ambré avec le sucre",
            "Ajoute la crème bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le praliné et le beurre une fois le caramel redescendu à 70 °C",
            "Mixe au mixeur plongeant pour une émulsion parfaite",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Praliné maison idéal (50 % fruits à coque minimum) ou purée "
            "pure pour un goût plus fin (noisette du Piémont, amande de "
            "Valence, pistache de Sicile, cacahuète). Le praliné apporte "
            "déjà du sucre, d'où l'importance de pousser le caramel bien "
            "ambré pour garder du caractère. Insert rêvé pour Paris-Brest, "
            "entremets noisette, royal caramel."
        ),
        'usages': ["Paris-Brest caramel", "entremets noisette-caramel", "royal praliné", "bonbon caramel-praliné"],
        'conservation': "7 jours au frigo dans un pot hermétique",
    },

    # ── 8. Infusé (version variable)
    {
        'key': 'caramel-infuse',
        'nom': 'Caramel Infusé',
        'total': 246,
        'ingredients': {
            'sucre': 100,
            'creme': 100,
            'beurre': 40,
            'ingredient-infusion': 5,
            'fleur-de-sel': 1,
        },
        'description': (
            "La version variable selon l'infusion. Fève tonka, thé matcha, "
            "bâton de réglisse, zestes d'agrumes, épices, fleurs, poivre "
            "Timut. Même procédé, parfum différent à chaque lot."
        ),
        'preparation': [
            "Porte la crème à frémissement et ajoute ton ingrédient d'infusion (fève tonka râpée, thé, réglisse, zestes…)",
            "Couvre et infuse hors du feu 15 à 30 minutes selon l'intensité voulue",
            "Filtre la crème infusée au chinois très fin et repèse pour retrouver 100 g",
            "Réalise un caramel bien ambré avec le sucre",
            "Ajoute la crème infusée bien chaude (attention aux projections)",
            "Laisse cuire quelques minutes jusqu'à épaississement, idéalement 107 °C",
            "Ajoute le beurre une fois le caramel redescendu à 70 °C et mixe au mixeur plongeant",
            "Termine avec la fleur de sel",
        ],
        'notes': (
            "Dosages d'infusion indicatifs : 1 fève tonka râpée, 10 g de "
            "thé matcha, 5 g de réglisse en morceaux, les zestes de 2 "
            "agrumes, 1 bâton de cannelle, 2 g de poivre Timut concassé. "
            "Goûte la crème infusée avant de poursuivre. Si trop fort, "
            "dilue avec de la crème neuve. Si trop faible, re-infuse 10 min."
        ),
        'usages': ["entremets signature", "déclinaison saisonnière", "bonbon d'auteur", "création perso"],
        'conservation': "7 jours au frigo dans un pot hermétique",
    },
]


# ──────────────────────────────────────────────────────────────
# RENDERER
# ──────────────────────────────────────────────────────────────

INTRO = (
    "Le caramel onctueux, c'est la signature gourmande par excellence : "
    "infusé, nappant, profond. Huit déclinaisons qui partagent exactement la "
    "même technique de base : caramel ambré, crème chaude, cuisson 107 °C, "
    "beurre à 70 °C, mixeur plongeant, fleur de sel. Une fois la base "
    "maîtrisée, tu décline à l'infini."
)

CLOTURE = (
    "La règle universelle : 107 °C au thermomètre pour la texture, 70 °C "
    "pour incorporer beurre et chocolat, mixeur plongeant 1 min pour "
    "l'émulsion. Un caramel trop clair reste trop sucré et fade. Un "
    "caramel trop brûlé devient amer et coupe en bouche. Vise l'ambré "
    "cuivré, le point où ça commence à fumer légèrement."
)


def _build_usages_note(r):
    parts = []
    if r.get('usages'):
        u = r['usages']
        if isinstance(u, list):
            parts.append("Usages : " + ", ".join(u))
    if r.get('conservation'):
        parts.append(f"Conservation : {r['conservation']}")
    return '. '.join(parts) if parts else None


def _content(story):
    s = styles()

    # Intro
    story.append(Spacer(1, 10))
    story.append(Paragraph("Caramels", s['h2']))
    story.append(gold_line(0.4, 2, 10))
    story.append(Paragraph(INTRO, s['body']))
    story.append(Spacer(1, 14))

    # Table of contents (8 recipes)
    story.append(Paragraph('§ Dans ce guide', s['h3']))
    story.append(gold_line(0.3, 2, 6))
    for r in CARAMELS:
        meta_str = f" · {r['total']} g"
        story.append(Paragraph(
            f'<link href="#recipe-{r["key"]}" color="#C8A04A">'
            f'→ {r["nom"]}</link>'
            f'<font color="#8A7D72" size="8">{meta_str}</font>',
            s['body']
        ))
    story.append(Spacer(1, 4))

    # Recipe cards, one per page
    for r in CARAMELS:
        story.append(PageBreak())
        notes = r.get('notes') or _build_usages_note(r)
        meta_extras = []
        if r.get('conservation'):
            m = re.match(r'^(\d+)\s*jour', r['conservation'])
            if m:
                meta_extras.append(f"Conservation {m.group(1)} j")

        story.extend(recipe_card(
            r['nom'],
            anchor=f'recipe-{r["key"]}',
            total=r['total'],
            ingredients=r['ingredients'],
            preparation=r['preparation'],
            description=r['description'],
            notes=notes,
            meta_extras=meta_extras,
        ))

    # Closing callout
    story.append(PageBreak())
    story.append(Spacer(1, 80))
    story.append(gold_callout("Garde ça en tête", CLOTURE))


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    build_pdf(
        OUT_PATH,
        title='Caramels',
        subtitle="Vanille, chocolats (noir/lait/blanc), café, fruits, praliné, infusé — huit déclinaisons d'une même base",
        running_header='Caramels',
        overline_text="MÉTHODE FONDATIONS PRO  ·  Crèmes · Caramels",
        tagline="— Geoffrey —",
        content_fn=_content,
    )


if __name__ == '__main__':
    main()
