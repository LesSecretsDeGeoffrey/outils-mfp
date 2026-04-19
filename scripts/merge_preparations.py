"""
Merge /tmp/preparations-fondations.json into data/recettes-geoffrey.json.
Adds : description, usages (if missing), preparation
Run   : python3 scripts/merge_preparations.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MAIN = os.path.join(ROOT, 'data', 'recettes-geoffrey.json')
PREPS = '/tmp/preparations-fondations.json'


def main():
    with open(MAIN, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(PREPS, 'r', encoding='utf-8') as f:
        preps = json.load(f)

    sections = ['biscuits', 'pates-a-tarte', 'pate-a-choux',
                'macarons', 'cremes-garnitures']
    added = 0
    skipped_keys = []

    for section in sections:
        if section not in data or section not in preps:
            continue
        src = data[section]
        enrichment = preps[section]
        for key, prep_data in enrichment.items():
            if key not in src:
                skipped_keys.append(f"{section}/{key}")
                continue
            if not isinstance(prep_data, dict):
                continue
            target = src[key]
            if 'description' in prep_data and 'description' not in target:
                target['description'] = prep_data['description']
            if 'usages' in prep_data and 'usages' not in target:
                target['usages'] = prep_data['usages']
            if 'preparation' in prep_data:
                target['preparation'] = prep_data['preparation']
                added += 1
            # macarons has an extra "cuisson" field in prep data — already in source

    # Macarons astuces / faq are meta-entries — copy them over if absent
    if 'macarons' in preps:
        for meta_key in ('astuces', 'faq'):
            if meta_key in preps['macarons'] and meta_key not in data.get('macarons', {}):
                data['macarons'][meta_key] = preps['macarons'][meta_key]

    with open(MAIN, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'✓ Merge terminé. {added} recettes enrichies avec preparation.')
    if skipped_keys:
        print(f'  Skipped (clés absentes dans source) : {skipped_keys}')


if __name__ == '__main__':
    main()
