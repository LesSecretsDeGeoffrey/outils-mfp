"""
Parse the original 'Guide Ultime Ganache montées' PDF and extract the full
PRÉPARATION steps for each ganache. Outputs a JSON that maps a normalized
name → list of steps, for merging back into data/recettes-geoffrey.json.

Run : python3 scripts/parse_ganaches_pdf.py
Output : /tmp/ganaches-preparations.json
"""
import re
import subprocess
import json
import unicodedata
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SRC_PDF = '/Users/geoffrey/Documents/Claude/PDF RESSOURCES/Copie de Guide Ultime Ganache montées (1).pdf'
OUT = '/tmp/ganaches-preparations.json'


def slugify(name):
    """Transform 'Ganache à la Vanille' → 'ganache-vanille' (roughly)."""
    s = unicodedata.normalize('NFD', name)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    # Drop common filler words for easier matching
    s = re.sub(r'-(a|la|le|les|de|du|des|et)-', '-', s)
    s = re.sub(r'^(a|la|le|les|de|du|des|et)-', '', s)
    s = re.sub(r'-(a|la|le|les|de|du|des|et)$', '', s)
    s = re.sub(r'--+', '-', s)
    return s.strip('-')


def extract_text(pdf_path):
    """Run pdftotext and return the layout-preserving text."""
    result = subprocess.run(
        ['pdftotext', '-layout', pdf_path, '-'],
        capture_output=True, text=True, check=True
    )
    return result.stdout


def parse_blocks(text):
    """Split text into ganache blocks. Each block starts at a 'Ganache X'
    heading and ends at the next one (or EOF). Returns list of (name, body)
    tuples."""
    lines = text.splitlines()
    # Identify candidate title lines (standalone 'Ganache …' or 'Namelaka …')
    title_re = re.compile(r'^\s*(Ganache|Namelaka)\b')
    blocks = []
    current_title = None
    current_body = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if title_re.match(line):
            # Flush previous block
            if current_title is not None:
                blocks.append((current_title, '\n'.join(current_body)))
            # Assemble multi-line title : consume consecutive indented non-numbered
            # non-INGRÉDIENTS lines that don't look like body text
            title_parts = [line.strip()]
            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if not nxt:
                    j += 1
                    continue
                if nxt.startswith(('INGRÉDIENTS', 'PRÉPARATION', '▢', '1.')):
                    break
                if re.match(r'^\d+[\.\)]', nxt):
                    break
                # Likely a title continuation if short (< 40 chars) and not sentence-ish
                if len(nxt) <= 40 and '.' not in nxt:
                    title_parts.append(nxt)
                    j += 1
                    continue
                break
            current_title = ' '.join(title_parts)
            current_body = []
            i = j
            continue
        current_body.append(line)
        i += 1
    if current_title is not None:
        blocks.append((current_title, '\n'.join(current_body)))
    return blocks


_STEP_RE = re.compile(r'^\s*(\d+)[\.\)]\s*(.*)$')


def parse_preparation(body):
    """Extract numbered steps from the block body. Returns list of strings."""
    # Find the PRÉPARATION marker
    idx = body.find('PRÉPARATION')
    if idx < 0:
        # Sometimes the PDF uses 'Préparation' (capitalized but lowercase rest)
        idx = body.find('Préparation')
    if idx < 0:
        return []
    tail = body[idx:]
    lines = tail.splitlines()
    steps = {}  # map step num → accumulated text
    current_num = None
    for line in lines:
        if 'PRÉPARATION' in line.upper():
            continue
        m = _STEP_RE.match(line)
        if m:
            current_num = int(m.group(1))
            steps[current_num] = m.group(2).strip()
        elif current_num is not None:
            stripped = line.strip()
            if stripped:
                # Continuation of previous step
                steps[current_num] = (steps[current_num] + ' ' + stripped).strip()
    # Sort by step number
    return [steps[n] for n in sorted(steps.keys())]


def main():
    text = extract_text(SRC_PDF)
    blocks = parse_blocks(text)
    print(f'Found {len(blocks)} title blocks')

    preparations = {}
    for title, body in blocks:
        steps = parse_preparation(body)
        if not steps:
            print(f"  skip (no prep) : {title!r}")
            continue
        slug = slugify(title)
        preparations[slug] = {
            'title': title,
            'preparation': steps,
        }

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(preparations, f, ensure_ascii=False, indent=2)
    print(f'✓ {len(preparations)} préparations extraites → {OUT}')
    for slug in sorted(preparations.keys()):
        print(f'  {slug:50}  ({len(preparations[slug]["preparation"])} steps)')


if __name__ == '__main__':
    main()
