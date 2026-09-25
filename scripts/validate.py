"""Check portable packaging and exact parity."""
import importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync_skills',ROOT/'scripts/sync_skills.py')
sync_skills=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync_skills)
drift=sync_skills.sync(check=True)
assert not drift,'Host copies have drifted from the canonical source:\n  '+'\n  '.join(drift)
CANONICAL=ROOT/sync_skills.CANONICAL
skills=sorted(folder for folder in CANONICAL.iterdir() if folder.is_dir())
for folder in skills:
    text=(folder/'SKILL.md').read_text()
    assert text.startswith('---\n') and f'name: {folder.name}\n' in text
    assert re.search(r'^description: .+',text,re.M)
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*',folder.name),folder.name
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if not link.startswith('http'): assert (folder/link).exists(),link
for path in ROOT.rglob('*.json'):
    if 'node_modules' not in path.parts: json.loads(path.read_text())
config=json.loads((ROOT/'plugins/dreamlayer/.mcp.json').read_text())
assert config['mcpServers']['dreamlayer']['args']==['-y','@dreamlayer/mcp@0.4.0-beta.4']
assert len(skills)==9

clawhub=ROOT/'clawhub/dreamlayer-image-workflows/SKILL.md'
text=clawhub.read_text()
assert text.startswith('---\n') and 'name: dreamlayer-image-workflows\n' in text
assert '@dreamlayer/mcp@0.4.0-beta.4' in text and '0.4.0-beta.3' not in text
assert 'dreamlayer_cancel' not in text
for folder in skills:
    assert folder.name in text, f'ClawHub entry point does not route to {folder.name}'
for doc in ('docs/copilot-setup.md','docs/cline-setup.md'):
    body=(ROOT/doc).read_text()
    for folder in skills:
        assert folder.name in body, f'{doc} does not list {folder.name}'
    assert '@dreamlayer/mcp@0.4.0-beta.4' in body and 'Unity' in body
print(f'PASS: {len(skills)} skills, valid JSON/links, pinned MCP, host copies identical to '
      f'{sync_skills.CANONICAL} ({", ".join(sync_skills.MIRRORS)}), ClawHub and host docs route to all of them')
