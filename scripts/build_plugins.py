"""Regenerate self-contained plugins from the canonical skills."""
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'.agents/skills'
for skill in source.iterdir():
    if skill.is_dir():
        shutil.copyfile(ROOT/'docs/workflow-contract.md',skill/'references/workflow-contract.md')
        if skill.name in ('godot-sprite-import','unity-sprite-import'):
            (skill/'scripts').mkdir(exist_ok=True)
            shutil.copyfile(ROOT/'scripts/import_sprite.py',skill/'scripts/import_sprite.py')
        shutil.copytree(skill,ROOT/'plugins/dreamlayer/skills'/skill.name,dirs_exist_ok=True)
print(f'Built {len(list(source.iterdir()))} skills')
