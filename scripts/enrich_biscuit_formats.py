"""
Enrichit chaque biscuit avec une dimension claire (Ø X cm ou tapis X × Y cm)
dans data/recettes-geoffrey.json.

Run : python3 scripts/enrich_biscuit_formats.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MAIN = os.path.join(ROOT, 'data', 'recettes-geoffrey.json')

# Mapping : key → format de référence Geoffrey (cercle/cadre/tapis)
# Source : outils-mfp/calculateur-moule-ideal.html tips
BISCUIT_FORMATS = {
    'genoise-nature':       {'diametre-cm': 20},
    'genoise-cacao':        {'diametre-cm': 20},
    'dacquoise':            {'diametre-cm': 20},
    'dacquoise-cacao':      {'diametre-cm': 20},
    'financier':            {'diametre-cm': 20},
    'financier-cacao':      {'diametre-cm': 20},
    'financier-praline':    {'diametre-cm': 20},
    'madeleine':            {'nombre': '18-20 madeleines', 'diametre-cm': 20},
    'madeleine-cacao':      {'nombre': '18-20 madeleines', 'diametre-cm': 20},
    'madeleine-praline':    {'nombre': '18-20 madeleines', 'diametre-cm': 20},
    'brownie':              {'cadre-cm': '20 × 20'},
    'brownie-lait':         {'cadre-cm': '20 × 20'},
    'brownie-blanc':        {'cadre-cm': '20 × 20'},
    'savoie':               {'diametre-cm': 20},
    'savoie-cacao':         {'diametre-cm': 20},
    'sacher':               {'diametre-cm': 20},
    'sacher-cacao':         {'diametre-cm': 20},
    'joconde':              {'tapis-cm': '40 × 30', 'diametre-cm': 20},
    'joconde-cacao':        {'tapis-cm': '40 × 30', 'diametre-cm': 20},
    'pain-de-genes':        {'diametre-cm': 16},
    'pain-de-genes-cacao':  {'diametre-cm': 16},
    'viennois':             {'tapis-cm': '40 × 30'},
    'viennois-cacao':       {'tapis-cm': '40 × 30'},
    'trocadero':            {'diametre-cm': 16},
    'trocadero-cacao':      {'diametre-cm': 16},
    'pate-a-choux-japonais':{'tapis-cm': '40 × 30'},
    'pate-a-choux-cacao':   {'tapis-cm': '40 × 30'},
}


def main():
    with open(MAIN, 'r', encoding='utf-8') as f:
        data = json.load(f)

    biscuits = data.get('biscuits', {})
    updated = 0
    missing = []

    for key, fmt in BISCUIT_FORMATS.items():
        if key not in biscuits:
            missing.append(key)
            continue
        biscuits[key]['format-reference'] = fmt
        updated += 1

    unmapped = [k for k in biscuits if k not in BISCUIT_FORMATS]

    with open(MAIN, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'✓ {updated} biscuits enrichis avec format-reference.')
    if missing:
        print(f'  Clés manquantes dans JSON : {missing}')
    if unmapped:
        print(f'  Biscuits sans mapping : {unmapped}')


if __name__ == '__main__':
    main()
