"""Check portable packaging and exact parity."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
count=0
for folder in (ROOT/'.agents/skills').iterdir():
    text=(folder/'SKILL.md').read_text()
    assert text.startswith('---\n') and f'name: {folder.name}\n' in text
    assert re.search(r'^description: .+',text,re.M)
    for file in folder.rglob('*'):
        if file.is_file():
            copy=ROOT/'plugins/dreamlayer/skills'/file.relative_to(ROOT/'.agents/skills')
            assert copy.read_bytes()==file.read_bytes(),f'Drift: {file}'
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if not link.startswith('http'): assert (folder/link).exists(),link
    count+=1
for path in ROOT.rglob('*.json'):
    if 'node_modules' not in path.parts: json.loads(path.read_text())
config=json.loads((ROOT/'plugins/dreamlayer/.mcp.json').read_text())
assert config['mcpServers']['dreamlayer']['args']==['-y','@dreamlayer/mcp@0.4.0-beta.4']
assert count==9

clawhub=ROOT/'clawhub/dreamlayer-image-workflows/SKILL.md'
text=clawhub.read_text()
assert text.startswith('---\n') and 'name: dreamlayer-image-workflows\n' in text
assert '@dreamlayer/mcp@0.4.0-beta.4' in text and '0.4.0-beta.3' not in text
assert 'dreamlayer_cancel' not in text
for folder in (ROOT/'.agents/skills').iterdir():
    assert folder.name in text, f'ClawHub entry point does not route to {folder.name}'
print(f'PASS: {count} skills, valid JSON/links, pinned MCP, identical copies, ClawHub entry point routes to all of them')

