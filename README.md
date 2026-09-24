# DreamLayer agent workflows

Generate and edit images from your agent, then save the files into your project.

Use DreamLayer for logo and app-icon concepts, product imagery, marketing visuals, print artwork concepts, background removal, upscaling, and reference-based sprite animations. These workflows use the same API, CLI and MCP tools.

## Install skills
```sh
npx skills add TheDesignFounder/dreamlayer-agent-plugin
```

Choose the workflows you need. The canonical source is `.agents/skills/`. Installing skills provides instructions; configure DreamLayer separately with an API key and credits.

## Connect the tools
Requires Node.js 22.12 or later. Get your key at [DreamLayer Platform](https://platform.dreamlayer.io/?utm_source=github&utm_medium=agent_distribution&utm_campaign=agent_launch&utm_content=readme).
Use `@dreamlayer/mcp@0.4.0-beta.3` for this full workflow set. The stable 0.3.0 tag does not cover sprites.

See [client setup](docs/client-setup.md) for Claude Code, Codex, Cursor, OpenCode, Copilot and Gemini CLI.

## What you can make
| Task | Workflow | Output and scope |
| --- | --- | --- |
| Original image or edit | generate-or-edit-image | Image file; inspect the result |
| Logos and app icons | logo-and-app-icon-concepts | Raster concepts, not vector masters |
| Product photos | product-image-generation | Reference-based concepts; review product fidelity |
| Shirts, stickers, posters | print-on-demand-artwork | Artwork concepts; check supplier dimensions |
| Ads and social posts | marketing-image-variations | Creative files, no ad publishing |
| Repeated photo operations | batch-photo-editing | Per-file jobs with a total budget |
| Sprite animations | sprite-sheet-from-reference | Beta ZIP, PNG frames, atlas and preview |
| Godot / Unity | godot-sprite-import / unity-sprite-import | Local engine import examples |

## Cost and recovery
Read capabilities and balance before paid work. Standard image operations currently cost one credit each. Sprite pricing depends on frame count: 7 frames currently quote 5.8 credits; 12 quote 9.9. Use the live quote and your approved cap. A new API account starts at zero credits.

Interrupted work resumes from its saved execution ID. Downloading a completed job does not start a replacement generation. [Workflow contract](docs/workflow-contract.md) · [API documentation](https://docs.dreamlayer.io/agent-api)

## Maintain one source
Edit `.agents/skills/`, then run `python3 scripts/build_plugins.py` to regenerate the plugin copies. Run `python3 scripts/validate.py` before publishing. Generated copies must match the canonical skills.

[Support](mailto:Mackenzie@dreamlayer.io) · [Terms](https://dreamlayer.io/terms) · [Privacy](https://dreamlayer.io/privacy)

