import re
import json

with open('js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Remove single-line comments (safe: no "//" inside our data strings) ──
content = re.sub(r'//[^\n]*', '', content)

# ── 2. Quote unquoted JS property names (whitelist only) ──
# Using a strict whitelist avoids accidentally quoting words like "Unique" that
# appear in description strings followed by " :".
PROPS = [
    'name', 'img', 'emoji', 'epithet', 'gender', 'affil', 'origin',
    'fruit', 'haki', 'status', 'arc', 'bounty', 'file', 'captain',
    'type', 'translated', 'description', 'holder', 'id', 'artist', 'yt',
]
for prop in PROPS:
    # Only quote if NOT preceded by a quote or word char (not already quoted)
    content = re.sub(r'(?<!["\w])\b' + prop + r'\b(?=\s*:(?!:))', f'"{prop}"', content)

# ── 3. Remove trailing commas before ] or } ──
content = re.sub(r',(\s*[}\]])', r'\1', content)


def extract_block(text, varname, open_br, close_br):
    """Extract the bracketed block of `const VARNAME = [...]` or `{...}`."""
    pattern = r'const\s+' + re.escape(varname) + r'\s*=\s*' + re.escape(open_br)
    m = re.search(pattern, text)
    if not m:
        raise ValueError(f"Could not find: const {varname}")
    start = m.end() - 1      # index of the opening bracket
    depth = 0
    for i in range(start, len(text)):
        if text[i] == open_br:
            depth += 1
        elif text[i] == close_br:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError(f"Unbalanced brackets for {varname}")


results = {}
specs = [
    ('ARCS',       '[', ']'),
    ('CHARACTERS', '[', ']'),
    ('FLAGS',      '[', ']'),
    ('ALIASES',    '{', '}'),
    ('FRUITS',     '[', ']'),
    ('OPENINGS',   '[', ']'),
]

all_ok = True
for varname, ob, cb in specs:
    try:
        block = extract_block(content, varname, ob, cb)
        parsed = json.loads(block)
        results[varname] = parsed
        count = len(parsed)
        print(f'OK  {varname}: {count} entries')
    except Exception as e:
        print(f'ERR {varname}: {e}')
        # Print around error for debugging
        if isinstance(e, json.JSONDecodeError):
            snippet = block[max(0, e.pos-60):e.pos+60]
            print(f'    Around error: ...{snippet!r}...')
        all_ok = False

if all_ok:
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print('\ndata.json written successfully!')
else:
    print('\nErrors encountered — data.json NOT written.')
