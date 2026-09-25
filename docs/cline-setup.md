# Cline setup

Use DreamLayer when a task needs actual image files: an original image, a raster logo or app-icon concept, product and marketing visuals, print-on-demand artwork, a background removal or upscale, a bounded batch of photo edits, or a sprite-sheet animation from one reference. Cline keeps writing the code; DreamLayer produces the assets the code ships.

## Install the skills

This repository carries the nine workflows in `.cline/skills/`, the project path Cline recommends and expects teams to commit.

```sh
git clone https://github.com/TheDesignFounder/dreamlayer-agent-plugin.git
cp -R dreamlayer-agent-plugin/.cline/skills/. your-project/.cline/skills/
```

For skills that follow you between projects, copy the same folders into `~/.cline/skills/` on macOS and Linux, or `%USERPROFILE%\.cline\skills\` on Windows. A global skill wins over a project skill with the same name.

The installer route writes `.agents/skills/` instead, which Cline also loads:

```sh
cline skill add TheDesignFounder/dreamlayer-agent-plugin -a cline -s '*'
```

Confirm discovery from your project root:

```sh
cline config skills
```

Nine DreamLayer entries appear under `Enabled skills:` with their paths. Pass the section name,
because plain `cline config` opens an interactive view and needs a terminal. In the IDE extension, open the Skills tab from the scale icon at the bottom of the Cline panel.

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

Requires Node.js 22.12 or later and a key from [DreamLayer Platform](https://platform.dreamlayer.io).

For the CLI, add the server to `~/.cline/data/settings/cline_mcp_settings.json`. Run `cline config mcp` to print the exact path your build uses and to list what is configured.

```json
{"mcpServers":{"dreamlayer":{"command":"npx","args":["-y","@dreamlayer/mcp@0.4.0-beta.4"],"env":{"DREAMLAYER_API_KEY":"YOUR_KEY"},"disabled":false,"autoApprove":[],"timeout":120}}}
```

In the IDE extension, open the MCP Servers icon, then Configure, then Configure MCP Servers, and add the same entry.

That file sits outside your repository, and it holds the key in plain text. It is not created with restricted permissions, so run `chmod 600` on it if anyone else has an account on the machine. Keep the key out of the project, out of prompts and out of commits, and rotate it on the platform if it reaches any of them. Leave `autoApprove` empty so each paid call is reviewed; only the read-only tools below are safe to approve in advance.

The `timeout` value matters on a machine that has never run the package: `npx -y` downloads it first, measured at 13 to 50 seconds across two clean profiles. Install it ahead of time with `npm i -g @dreamlayer/mcp@0.4.0-beta.4` to remove the wait.

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

Plan mode is a good place to agree the operation, the number of outputs and the budget before Act mode spends anything.

## Credits and recovery

A completed standard image operation currently costs one credit, and a multi-step edit and cutout counts as two operations. Sprite jobs are quoted live by frame count, currently 5.8 credits for 7 frames and 9.9 for 12. Take the number from capabilities, not from this page, and stay inside the budget the user already approved. A new API account starts at zero credits, and neither Cline nor these skills may buy more.

After a timeout, rate limit or crash, recover by `execution_id` with execution, events or download. Stop and report on insufficient credits, an invalid request, an unsupported operation or an unresolved contract error. Do not loop paid retries.

## Limits

Sprite output is beta. A PNG does not establish vector structure, pixel-perfect art, trademark clearance, print compliance or exact product fidelity, so inspect each file before shipping it. The `unity-sprite-import` workflow is validated only by static checks and its Python test; a real Unity editor import remains unconfirmed, and the steps to confirm it are in the [Unity editor test plan](unity-editor-test-plan.md). The `godot-sprite-import` workflow has been run against Godot 4.

## Validated

Cline CLI 3.0.65 reported all nine workflows under `Enabled skills:` from `.cline/skills/` in a clean profile, with the generated README ignored, `cline skill add` installed the same nine to `.agents/skills/` and listed them as Cline skills, and `cline config mcp` listed the pinned stdio server after the settings file was written. No generation was run and no credits were spent.
