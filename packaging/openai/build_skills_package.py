"""Build the skills-only package the OpenAI plugin portal uploads.

The portal's Skills step takes a ZIP whose root holds a portable Agent Plugins
manifest and a skills/ directory. Everything inside comes from the canonical
source, so this package can never describe workflows we do not ship. The build
is byte-reproducible: entries are sorted and timestamps fixed, which lets
scripts/validate.py fail when the committed ZIP drifts from the skills.

Usage: python3 packaging/openai/build_skills_package.py [--check]
"""
import io, json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / 'plugins/dreamlayer/skills'
PACKAGE = Path(__file__).resolve().parent / 'dreamlayer-skills-1.0.0.zip'
# Fixed so two builds of the same skills produce the same bytes.
TIMESTAMP = (2026, 1, 1, 0, 0, 0)
IGNORED = {'.DS_Store', '__pycache__'}
MANIFEST = {
    '$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
    'name': 'dreamlayer',
    'version': '1.0.0',
    'description': (
        'Generate and edit images, remove backgrounds, upscale, and build sprite-sheet '
        'animations, with the credit cost quoted before each job.'
    ),
    'author': {'name': 'Mackenzie Derival', 'email': 'Mackenzie@dreamlayer.io', 'url': 'https://dreamlayer.io'},
    'homepage': 'https://dreamlayer.io/agent',
    'repository': 'https://github.com/TheDesignFounder/dreamlayer-agent-plugin',
    'license': 'MIT',
    'keywords': ['image-generation', 'image-editing', 'sprite-sheets', 'logo-concepts', 'product-images'],
}


def contents():
    """The exact file map the package carries, sorted for reproducibility."""
    files = {'plugin.json': (json.dumps(MANIFEST, indent=2) + '\n').encode()}
    for path in sorted(CANONICAL.rglob('*')):
        relative = path.relative_to(CANONICAL)
        if path.is_file() and not IGNORED & set(relative.parts):
            files[f'skills/{relative.as_posix()}'] = path.read_bytes()
    return files


def build():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(contents().items()):
            info = zipfile.ZipInfo(name, date_time=TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def main(argv):
    built = build()
    if '--check' in argv:
        if not PACKAGE.exists():
            print(f'MISSING: {PACKAGE.relative_to(ROOT)}; run python3 packaging/openai/build_skills_package.py')
            return 1
        if PACKAGE.read_bytes() != built:
            print(f'DRIFT: {PACKAGE.relative_to(ROOT)} does not match the canonical skills; rebuild it')
            return 1
        print(f'{PACKAGE.name} matches {len(contents()) - 1} canonical files')
        return 0
    PACKAGE.write_bytes(built)
    print(f'wrote {PACKAGE.relative_to(ROOT)} ({len(built)} bytes, {len(contents())} entries)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
