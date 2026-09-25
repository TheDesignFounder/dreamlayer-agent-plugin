# GitHub Copilot setup

Use DreamLayer when a task needs actual image files: an original image, a raster logo or app-icon concept, product and marketing visuals, print-on-demand artwork, a background removal or upscale, a bounded batch of photo edits, or a sprite-sheet animation from one reference. Copilot keeps writing the code; DreamLayer produces the assets the code ships.

## Install the skills

This repository already carries the nine workflows in `.github/skills/`, which Copilot reads as project skills. Copilot also reads `.agents/skills/` and `.claude/skills/`, and this repository generates `.agents/skills/` from the same source.

```sh
git clone https://github.com/TheDesignFounder/dreamlayer-agent-plugin.git
cp -R dreamlayer-agent-plugin/.github/skills/. your-project/.github/skills/
```

For skills that follow you between projects, copy the same folders into `~/.copilot/skills/` or `~/.agents/skills/`, or run `copilot skill add <directory>`.

Confirm discovery from your project root:

```sh
copilot skill list
```

Nine DreamLayer entries appear under `Project skills:`. `copilot skill disable <name>` hides one you do not want.

## The nine workflows

| Workflow | Makes |
| --- | --- |
| generate-or-edit-image | An original image, an edit, a cutout or an upscale |
| logo-and-app-icon-concepts | Raster logo and app-icon directions, not vector masters |
| product-image-generation | Ecommerce backgrounds and lifestyle concepts from a product photo |
| print-on-demand-artwork | Shirt, sticker and poster artwork with transparent PNG preparation |
| marketing-image-variations | Ad, banner and social variations from a brief or reference |
| batch-photo-editing | One edit, cutout or upscale applied across a list of files, with a budget |
| sprite-sheet-from-reference | A sprite-sheet ZIP of transparent frames, atlas and preview |
| godot-sprite-import | A runnable Godot 4 demo from a downloaded sprite ZIP |
| unity-sprite-import | Unity 2D import files and a frame player from a downloaded sprite ZIP |

## Connect the tools

Requires Node.js 22.12 or later and a key from [DreamLayer Platform](https://platform.dreamlayer.io). What DreamLayer does, and what it costs, is on the [product page](https://dreamlayer.io/agent?utm_source=github_copilot&utm_medium=agent_distribution&utm_campaign=agent_launch_202609).

```sh
copilot mcp add dreamlayer --env DREAMLAYER_API_KEY=YOUR_KEY -- npx -y @dreamlayer/mcp@0.4.0-beta.4
copilot mcp list
```

The entry lands in `~/.copilot/mcp-config.json`, outside your repository. Copilot masks the value when it prints the server, but that file holds the key in plain text; it is created readable only by your own account. A workspace-level `.mcp.json` or `.github/mcp.json` works too, but those files are committed, so keep the key out of them. In VS Code use `.vscode/mcp.json` with a `promptString` input, as shown in [client setup](client-setup.md).

Never paste the key into a prompt, a skill file or a commit. Rotate it on the platform if it reaches any of those.

The first run downloads the package. On a machine that has never run it, allow 13 to 50 seconds before deciding the server failed, or install it ahead of time with `npm i -g @dreamlayer/mcp@0.4.0-beta.4`.

## The seven tools

| Tool | Use it for | Credits |
| --- | --- | --- |
| dreamlayer_capabilities | Supported operations, input limits, live sprite pricing | none |
| dreamlayer_balance | Available credits for this key | none |
| dreamlayer_upload_image | Register a local reference, returns input_asset_id | none |
| dreamlayer_generate | The paid call: text_to_image, image_to_image, background_remove, upscale, sprite_sheet | charged |
| dreamlayer_execution | Canonical status of an execution you already started | none |
| dreamlayer_events | Resume a dropped stream from last_event_id | none |
| dreamlayer_download | Write a finished image to an absolute new local path | none |

## Generate, poll or resume, download

1. Read capabilities and balance. Both are free and both must succeed before any paid call.
2. For an edit, cutout, upscale or sprite, call upload_image once and keep the `input_asset_id`.
3. Save a unique `idempotency_key` and the whole request locally, then call generate with an explicit operation. It returns `execution_id`, `status`, `asset`, `question` and `last_event_id`.
4. While the job runs, call execution or events with that `execution_id`. Never call generate again to check on a job; that starts a second paid run.
5. A `needs_input` result is a question, not a failure. Answer it with the `conversation_id`.
6. Call download with the `execution_id` and a new absolute path, then open the file. A returned URL is not proof that a local file exists.

## Credits and recovery

A completed standard image operation currently costs one credit, and a multi-step edit and cutout counts as two operations. Sprite jobs are quoted live by frame count, currently 5.8 credits for 7 frames and 9.9 for 12. Take the number from capabilities, not from this page, and stay inside the budget the user already approved. A new API account starts at zero credits, and neither Copilot nor these skills may buy more.

After a timeout, rate limit or crash, recover by `execution_id` with execution, events or download. Stop and report on insufficient credits, an invalid request, an unsupported operation or an unresolved contract error. Do not loop paid retries.

## Limits

Sprite output is beta. A PNG does not establish vector structure, pixel-perfect art, trademark clearance, print compliance or exact product fidelity, so inspect each file before shipping it. The `unity-sprite-import` workflow is validated only by static checks and its Python test; a real Unity editor import remains unconfirmed, and the steps to confirm it are in the [Unity editor test plan](unity-editor-test-plan.md). The `godot-sprite-import` workflow has been run against Godot 4.

## Validated

GitHub Copilot CLI 1.0.88 listed all nine workflows from `.github/skills/` in a clean profile with no sign-in, and `copilot mcp add` plus `copilot mcp list` registered the pinned server with the key masked in the output. No generation was run and no credits were spent.
