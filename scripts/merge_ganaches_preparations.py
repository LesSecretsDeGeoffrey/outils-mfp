"""
Merge parsed preparations (from /tmp/ganaches-preparations.json) back into
data/recettes-geoffrey.json, section ganaches-guide/{classiques,montees}.

Match strategy: normalize both sides (remove accents, filler words, lowercase)
and compare. Unmatched entries are reported.

Run : python3 scripts/merge_ganaches_preparations.py
"""
import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
PREP_JSON = '/tmp/ganaches-preparations.json'
DATA_JSON = os.path.join(ROOT, 'data', 'recettes-geoffrey.json')

FILLERS = {'a', 'la', 'le', 'les', 'de', 'du', 'des', 'et', 'au', 'aux', 'à', 'd', 'l'}


def norm(s):
    # Replace any apostrophe variant (straight, curly, etc) with a space BEFORE
    # ASCII filter, so d'oranger and d'oranger normalize to 'oranger'
    s = re.sub(r"[\u2019\u2018\u0027\u02BC\u02BB]", ' ', s)
    s = unicodedata.normalize('NFD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", ' ', s)
    words = [w for w in s.split() if w and w not in FILLERS]
    return ' '.join(words)


def main():
    with open(PREP_JSON, encoding='utf-8') as f:
        parsed = json.load(f)

    with open(DATA_JSON, encoding='utf-8') as f:
        data = json.load(f)

    gg = data.get('ganaches-guide', {})

    # Build a lookup : normalized title → (section, key, entry)
    lookup = {}
    for section in ('classiques', 'montees'):
        for key, entry in gg.get(section, {}).items():
            if isinstance(entry, dict) and 'nom' in entry:
                n = norm(entry['nom'])
                if n in lookup:
                    print(f"  [warning] duplicate norm title {n!r}")
                lookup[n] = (section, key)

    # Match parsed preps
    matched = 0
    unmatched = []
    for slug, payload in parsed.items():
        title = payload.get('title', '')
        n = norm(title)
        if n in lookup:
            section, key = lookup[n]
            gg[section][key]['preparation'] = payload['preparation']
            matched += 1
        else:
            unmatched.append((slug, title, n))

    print(f'\n✓ matched {matched} / {len(parsed)} ganaches')
    if unmatched:
        print(f'\n⚠ {len(unmatched)} unmatched :')
        for slug, title, n in unmatched:
            print(f'  slug={slug!r:45} title={title!r}')
            print(f'      normalized={n!r}')
            # Show close candidates
            candidates = [(ln, v) for ln, v in lookup.items() if ln[:8] == n[:8]]
            for ln, v in candidates[:5]:
                print(f'      close   ={ln!r} → {v}')

    # Report missing preparations
    print('\n--- ganaches still without preparation ---')
    missing = 0
    for section in ('classiques', 'montees'):
        for key, entry in gg.get(section, {}).items():
            if isinstance(entry, dict) and 'preparation' not in entry:
                missing += 1
                print(f'  {section}/{key:45} nom={entry.get("nom", "")!r}')
    print(f'({missing} missing)')

    # Write back
    with open(DATA_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'\n→ wrote {DATA_JSON}')


if __name__ == '__main__':
    main()
