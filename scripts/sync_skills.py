"""Generate every host skill directory from the one canonical source.

Canonical: plugins/dreamlayer/skills. Every other location is a byte-for-byte
copy produced here, so a workflow can never differ between hosts. Run without
arguments to regenerate, with --check to fail on drift (CI and validate.py).
"""
import sys
from pathlib import Path

CANONICAL = 'plugins/dreamlayer/skills'
MIRRORS = {
    '.agents/skills': 'Cursor, OpenCode, GitHub Copilot and the npx skills installer',
    '.github/skills': 'GitHub Copilot in the CLI, VS Code and the coding agent',
    '.cline/skills': 'Cline',
}
VENDORED = {'references/workflow-contract.md': 'docs/workflow-contract.md'}
ENGINE_SCRIPTS = {'godot-sprite-import', 'unity-sprite-import'}
IGNORED = {'.DS_Store', '__pycache__'}


def readme(purpose):
    return (
        '# Generated skills\n\n'
        'Do not edit these files. They are copied byte for byte from\n'
        f'`{CANONICAL}/`, the canonical source, so that {purpose} load the same\n'
        'workflows as every other host.\n\n'
        'Change a workflow in the canonical source, then regenerate:\n\n'
        '```sh\npython3 scripts/sync_skills.py\n```\n\n'
        '`python3 scripts/sync_skills.py --check` fails when any copy has drifted, and\n'
        '`python3 scripts/validate.py` runs that check.\n'
    )


def tracked(root):
    """Files under root, ignoring editor and interpreter leftovers."""
    return sorted(
        path for path in root.rglob('*')
        if path.is_file() and not IGNORED & set(path.relative_to(root).parts)
    )


def vendor(root, check):
    """Refresh the shared files each skill carries so it travels self-contained."""
    problems = []
    for skill in sorted(path for path in (root / CANONICAL).iterdir() if path.is_dir()):
        wanted = dict(VENDORED)
        if skill.name in ENGINE_SCRIPTS:
            wanted['scripts/import_sprite.py'] = 'scripts/import_sprite.py'
        for relative, source in wanted.items():
            data = (root / source).read_bytes()
            destination = skill / relative
            if destination.exists() and destination.read_bytes() == data:
                continue
            problems.append(f'{destination.relative_to(root)}: stale copy of {source}')
            if not check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
    return problems


def sync(root=None, check=False):
    """Return the drift found; write the mirrors too unless check is set."""
    root = Path(root or Path(__file__).resolve().parents[1])
    problems = vendor(root, check)
    canonical = {
        path.relative_to(root / CANONICAL): path.read_bytes()
        for path in tracked(root / CANONICAL)
    }
    for mirror, purpose in MIRRORS.items():
        target = root / mirror
        wanted = dict(canonical)
        wanted[Path('README.md')] = readme(purpose).encode()
        for relative, data in sorted(wanted.items()):
            destination = target / relative
            if destination.exists() and destination.read_bytes() == data:
                continue
            problems.append(
                f'{mirror}/{relative}: '
                + ('missing' if not destination.exists() else 'differs from the canonical source')
            )
            if not check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
        present = {path.relative_to(target) for path in tracked(target)} if target.exists() else set()
        for relative in sorted(present - set(wanted)):
            problems.append(f'{mirror}/{relative}: not in the canonical source')
            if not check:
                (target / relative).unlink()
        if not check and target.exists():
            for path in sorted(target.rglob('*'), reverse=True):
                if path.is_dir() and not any(path.iterdir()):
                    path.rmdir()
    return problems


def main(argv):
    check = '--check' in argv
    problems = sync(check=check)
    if problems and check:
        print('DRIFT:')
        for problem in problems:
            print(f'  {problem}')
        print(f'{len(problems)} problem(s). Run: python3 scripts/sync_skills.py')
        return 1
    root = Path(__file__).resolve().parents[1]
    skills = len([path for path in (root / CANONICAL).iterdir() if path.is_dir()])
    state = f'rewrote {len(problems)} file(s)' if problems else 'already matched'
    print(f'{skills} skills, {state}: {", ".join(MIRRORS)} (canonical {CANONICAL})')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
