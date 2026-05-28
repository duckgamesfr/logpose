import os

with open('css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()   # 1-indexed: line N = lines[N-1]

total = len(lines)
print(f'style.css: {total} lines')

# (output_filename, [(start_line, end_line), ...])  — line numbers are 1-based inclusive
SPLITS = [
    ('base.css',    [(1,    234)]),
    ('layout.css',  [(235,  547)]),
    ('modals.css',  [(548,  627), (1165, 1338), (1789, 1834)]),
    ('classic.css', [(628,  991)]),
    ('wanted.css',  [(992,  1121)]),
    ('flag.css',    [(1122, 1164)]),
    ('fruit.css',   [(1339, 1464)]),
    ('inf.css',     [(1465, 1504)]),
    ('emoji.css',   [(1505, 1632)]),
    ('misc.css',    [(1633, 1788), (1835, 1917)]),
    ('audio.css',   [(1918, total)]),
]

covered = 0
for fname, ranges in SPLITS:
    parts = []
    for start, end in ranges:
        parts.extend(lines[start - 1 : end])   # 0-based slicing
        covered += end - start + 1

    out_path = os.path.join('css', fname)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(parts)
    size = os.path.getsize(out_path)
    line_count = sum(end - start + 1 for start, end in ranges)
    print(f'  wrote css/{fname}  ({line_count} lines, {size} bytes)')

print(f'\nTotal lines covered: {covered} / {total}')
if covered == total:
    print('All lines covered — split is complete!')
else:
    print(f'WARNING: {total - covered} lines unaccounted for!')
