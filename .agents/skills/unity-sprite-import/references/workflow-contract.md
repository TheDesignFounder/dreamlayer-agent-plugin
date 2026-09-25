# DreamLayer workflow contract

Use the installed DreamLayer MCP tools, or the pinned CLI when MCP is unavailable.
Read the actual tool schema before calling. Never pass fields a client does not expose.

## Setup
Requires Node.js >=22.12 and a DreamLayer API key from https://platform.dreamlayer.io.
Install the supported sprite-capable beta: `npm install -g dreamlayer@0.4.0-beta.3`.
MCP: `npx -y @dreamlayer/mcp@0.4.0-beta.4`. Supply DREAMLAYER_API_KEY to the server process using the host's secret settings. Never commit keys or put them in prompts.
The stable npm tag remains 0.3.0. Do not claim it supports this complete workflow.

## Before paid work
1. Read dreamlayer_capabilities and dreamlayer_balance (or CLI capabilities/balance --json). If either fails, resolve it before spending.
2. Confirm the requested operation is advertised. Ordinary completed image operations currently cost one credit each; obtain the live cost from capabilities. A multi-step edit and cutout costs two operations.
3. Use the user's already-authorized operation, number of outputs and credit budget. Ask only if missing. Never buy credits or expand the batch implicitly.
4. For file operations, verify input readability and a new output path before submitting. Upload once using dreamlayer_upload_image; preserve its input_asset_id.
5. Save a unique idempotency_key and the complete request locally before each generation. Do not store credentials in the job record.

## Execute and recover
Select operation explicitly: text_to_image; image_to_image; background_remove; upscale; sprite_sheet.
All except text_to_image require input_asset_id. Generate returns execution_id, status, asset, question and last_event_id.
Preserve IDs/cursor after each response. For running work, call dreamlayer_execution or dreamlayer_events; do not generate a replacement after a timeout.
A needs_input result is a question, not a failed generation. Continue using conversation_id and respond.
For completed work, dreamlayer_download writes an absolute new local path. Never treat a returned asset URL as proof that the local file exists.
On a local download error, repair the destination and download the same execution.
File-based CLI retries upload a new asset; use status and download after uncertainty rather than rerunning the paid command.
Stop at insufficient credits, invalid request, unsupported operation, or an unresolved contract error. Keep recoverable state; do not loop paid retries.

## Output acceptance
Inspect the saved image or preview. Check dimensions, transparency if requested, text spelling, reference fidelity and the intended use. Label uninspected outputs.
PNG output does not establish SVG/vector structure, pixel-perfect art, trademark clearance, print compliance, exact product fidelity or consistent animation.
API documentation: https://docs.dreamlayer.io/agent-api
Recovery: https://docs.dreamlayer.io/agent-api/jobs-and-events

## CLI examples
```sh
dreamlayer capabilities --json
dreamlayer balance --json
dreamlayer generate "Original image brief" --aspect 1:1 --idempotency-key UNIQUE_SAVED_KEY --out concept.png --json
dreamlayer edit reference.png "Change the background to a simple studio scene" --idempotency-key UNIQUE_SAVED_KEY --out edited.png --json
dreamlayer cutout reference.png --idempotency-key UNIQUE_SAVED_KEY --out cutout.png --json
dreamlayer status EXECUTION_ID --json
dreamlayer download EXECUTION_ID --out recovered.png --json
```
Placeholder IDs and keys must be replaced. Check CLI --help for supported flags; --max-credits is for sprite jobs.

