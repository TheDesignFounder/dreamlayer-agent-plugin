#!/usr/bin/env python3
"""Build the Smithery-specific MCPB from the spec-compliant bundle.

Smithery never runs a local (stdio) bundle: its CLI copies `manifest.json.tools`
verbatim into the listing's server card, and the registry rejects tool entries
without `inputSchema`. The MCPB validator, however, only allows `name` and
`description` per tool. So we keep the spec-compliant bundle for GitHub/Claude
Desktop and derive a Smithery variant whose tool entries are the exact
`tools/list` output of the bundled runtime (captured by list_tools.mjs).

usage: build_smithery_bundle.py <spec.mcpb> <tools-list.json> <out.mcpb>
"""
import json, sys, zipfile

spec, tools_json, out = sys.argv[1:4]
lst = json.load(open(tools_json))
zin = zipfile.ZipFile(spec)
manifest = json.loads(zin.read("manifest.json"))
runtime = json.loads(zin.read("node_modules/@dreamlayer/mcp/package.json"))["version"]
assert lst["serverInfo"]["version"] == runtime, f"tools list is from {lst['serverInfo']['version']}, bundle runs {runtime}"
manifest["tools"] = [
    {k: t[k] for k in ("name", "description", "inputSchema", "outputSchema", "annotations") if t.get(k) is not None}
    for t in lst["tools"]
]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "manifest.json":
            data = json.dumps(manifest, indent=2).encode()
        zout.writestr(info, data)
print(f"wrote {out}: {len(manifest['tools'])} tools, runtime {runtime}, manifest version {manifest['version']}")
