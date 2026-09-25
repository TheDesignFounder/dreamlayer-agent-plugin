# Hermes Agent setup

Hermes installs skills from sources it already supports, so DreamLayer needs no separate
Hermes listing. Pick whichever source you prefer; all four serve the same canonical
workflows from this repository.

Hermes keeps skills in `~/.hermes/skills/` and follows the agentskills.io format, which is
what this repository publishes.

## Install one skill

From ClawHub:

```sh
hermes skills install clawhub/thedesignfounder/dreamlayer-image-workflows
```

Straight from this repository, by owner/repo/path:

```sh
hermes skills install TheDesignFounder/dreamlayer-agent-plugin/clawhub/dreamlayer-image-workflows
```

As a single file, which is the `url` source:

```sh
hermes skills install https://raw.githubusercontent.com/TheDesignFounder/dreamlayer-agent-plugin/main/clawhub/dreamlayer-image-workflows/SKILL.md
```

That entry point states setup, the seven tools, the generate-poll-download loop, the costs
and the limits, then routes each job to the matching workflow below.

## Install every workflow

Add this repository as a tap, then point it at the skills folder. `tap add` writes a new
tap with `path: "skills/"`, so edit the tap entry to `plugins/dreamlayer/skills` before
searching:

```sh
hermes skills tap add TheDesignFounder/dreamlayer-agent-plugin
hermes skills tap list
hermes skills search dreamlayer
```

Or install one workflow directly without a tap:

```sh
hermes skills install TheDesignFounder/dreamlayer-agent-plugin/plugins/dreamlayer/skills/sprite-sheet-from-reference
```

The nine workflows are `generate-or-edit-image`, `logo-and-app-icon-concepts`,
`product-image-generation`, `print-on-demand-artwork`, `marketing-image-variations`,
`batch-photo-editing`, `sprite-sheet-from-reference`, `godot-sprite-import` and
`unity-sprite-import`.

## Connect the tools

The skills call the DreamLayer MCP server. Add it to Hermes the same way you add any other
stdio MCP server, and give the key to the server process rather than your shell:

```json
{"mcpServers":{"dreamlayer":{"command":"npx","args":["-y","@dreamlayer/mcp@0.4.0-beta.4"],"env":{"DREAMLAYER_API_KEY":"YOUR_KEY"},"connectionTimeoutMs":90000}}}
```

The timeout matters on a first run: `npx -y` downloads the package before the server
answers, measured at 13 to 50 seconds across two clean profiles, and a host that waits
only a few seconds will call the server dead. Raise whichever key your host uses, or
install the package first with `npm i -g @dreamlayer/mcp@0.4.0-beta.4`.

Create the key at [platform.dreamlayer.io](https://platform.dreamlayer.io). Node.js 22.12 or
later is required. Without the key the server exits and names the missing variable.

Check the connection before any paid work:

- `dreamlayer_capabilities` reports the operations your key may run and spends nothing.
- `dreamlayer_balance` reports available credits and spends nothing.

## What to expect

Ordinary completed image operations currently cost one credit each; read the live figure
from capabilities. Sprite jobs are a beta with frame-based pricing. Work is asynchronous:
`dreamlayer_generate` returns an `execution_id`, and you poll `dreamlayer_execution` or
resume from `dreamlayer_events` before calling `dreamlayer_download`.

Godot import is validated end to end, including transparent frames, per-frame timing and a
looping cycle. Unity ships importer code and instructions; editor validation is not
confirmed. Nothing is published to a store for you, logo output is raster with no vector
export or trademark clearance, and print artwork still needs a print-spec review.

More detail: <https://dreamlayer.io/agent?utm_source=hermes&utm_medium=agent_distribution&utm_campaign=agent_launch_202609>
