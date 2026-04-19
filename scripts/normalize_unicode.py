"""
Normalize JSON strings to characters renderable by Helvetica/Times base fonts.
Removes superscript modifiers, fractions, variation selectors and emojis that
appear as tofu (■) in ReportLab-generated PDFs.

Run : python3 scripts/normalize_unicode.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
MAIN = os.path.join(ROOT, 'data', 'recettes-geoffrey.json')

# Character substitutions (not rendered by base fonts → readable plain text)
SUBS = {
    # Superscript modifier letters
    'ᵉ': 'e',       # U+1D49 MODIFIER LETTER SMALL E (1/10ᵉ)
    'ᵃ': 'a',
    'ᵒ': 'o',
    'ᵈ': 'd',
    'ʳ': 'r',
    'ⁿ': 'n',
    'ᵗ': 't',
    'ⁱ': 'i',
    'ˢ': 's',
    # Fractions
    '½': '1/2',
    '¼': '1/4',
    '¾': '3/4',
    '⅓': '1/3',
    '⅔': '2/3',
    '⅛': '1/8',
    # Invisible modifier (usually attached to an emoji)
    '\ufe0f': '',
    # Emoji replacements (tofu otherwise)
    '⚠': 'Attention :',
    '✓': 'OK',
    '✗': 'X',
    # Non-breaking thin space (avoid issues with text wrapping)
    '\u202f': ' ',
    '\u00a0': ' ',
}


def normalize(obj):
    if isinstance(obj, str):
        for bad, good in SUBS.items():
            if bad in obj:
                obj = obj.replace(bad, good)
        return obj
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    return obj


def main():
    with open(MAIN, 'r', encoding='utf-8') as f:
        data = json.load(f)

    counts = {}
    def scan(x):
        if isinstance(x, str):
            for ch in SUBS:
                n = x.count(ch)
                if n:
                    counts[ch] = counts.get(ch, 0) + n
        elif isinstance(x, dict):
            for v in x.values():
                scan(v)
        elif isinstance(x, list):
            for v in x:
                scan(v)
    scan(data)

    normalized = normalize(data)
    with open(MAIN, 'w', encoding='utf-8') as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    if counts:
        print('Caractères remplacés :')
        for ch, n in counts.items():
            print(f"  {repr(ch):10} → {repr(SUBS[ch])}  ({n}x)")
    else:
        print('Aucun caractère à normaliser.')


if __name__ == '__main__':
    main()
