#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Mapping extension/type to target folder
MOVE_MAP = {
    '.py': 'src/app/',
    '.js': 'src/static/js/',
    '.css': 'src/static/css/',
    '.ttf': 'src/static/fonts/',
    '.svg': 'src/static/images/',
    '.png': 'src/static/images/',
    '.jpg': 'src/static/images/',
    '.jpeg': 'src/static/images/',
    '.html': 'src/templates/',
    '.md': 'docs/',
}

EXCLUDE = {'src', 'scripts', 'tests', 'docs', 'deployment', 'config', 'static', 'templates', '.git', '.venv', '__pycache__'}

ROOT = Path(__file__).parent.parent

for item in ROOT.iterdir():
    # Ne jamais déplacer le README.md de la racine
    if item.is_file() and item.name.lower() == 'readme.md':
        continue
    if item.is_file() and item.suffix in MOVE_MAP:
        target = ROOT / MOVE_MAP[item.suffix]
        target.mkdir(parents=True, exist_ok=True)
        shutil.move(str(item), str(target / item.name))
        print(f"Moved {item.name} -> {target}")
    elif item.is_dir() and item.name not in EXCLUDE:
        # Optionally move all .py files in custom folders to src/app
        for pyfile in Path(item).rglob('*.py'):
            target = ROOT / 'src/app/'
            target.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pyfile), str(target / pyfile.name))
            print(f"Moved {pyfile} -> {target}")

print("Organisation terminée.")
