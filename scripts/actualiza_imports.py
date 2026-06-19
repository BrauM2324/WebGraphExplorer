import os

replacements = [
    ('from crawler.', 'from rastreador.'),
    ('import crawler.', 'import rastreador.'),
    ('from search_algorithms.', 'from algoritmos_busqueda.'),
    ('import search_algorithms.', 'import algoritmos_busqueda.'),
    ('from utils.', 'from utilidades.'),
    ('import utils.', 'import utilidades.'),
    ('from results.', 'from resultados.'),
    ('import results.', 'import resultados.'),
]

root = '.'
changed = 0
for dirpath, dirnames, filenames in os.walk(root):
    # skip .git and __pycache__ and scripts
    if any(part.startswith('.') or part == '__pycache__' for part in dirpath.split(os.sep)):
        continue
    for fname in filenames:
        if not fname.endswith('.py'):
            continue
        path = os.path.join(dirpath, fname)
        if path.startswith('.\\scripts') or path.startswith('./scripts'):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        new = text
        for a, b in replacements:
            new = new.replace(a, b)
        if new != text:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new)
            print('Updated:', path)
            changed += 1

print('Total files changed:', changed)
