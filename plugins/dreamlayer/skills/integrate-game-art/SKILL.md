---
name: integrate-game-art
description: "Plan, obtain, validate, and integrate DreamLayer artwork into a playable game while preserving its mechanics. Use when a game needs background, character, UI, or sprite files; not for gameplay-only work or another image service."
---

# Integrate game art

Inspect the game before requesting art: engine and import settings, logical world units,
collision bodies, pivots, sprite dimensions, alpha requirements, animation timing, camera,
and asset paths. Separate visual dimensions from physics dimensions. Keep a playable
geometry baseline and record the behavior that must survive the artwork swap.

Read the bundled [workflow contract](references/workflow-contract.md) for supported clients,
authentication, billing, polling, download, and recovery. Installation supplies instructions;
it does not connect or authenticate an MCP server. Inspect the actual available tool schema.
If the connected client lacks download or sprite fields, use the supported client from that
contract, or retain bundled assets and report the limitation.

## Plan and obtain

- Inventory reusable artwork and its license/provenance first. A downloaded sample is not
  a new generation. Code-authored scenery should be labeled separately from DreamLayer art.
- Produce a dry-run asset plan with role, output path, dimensions/aspect, reference, operation,
  transparency, and estimated credits. Read live capabilities and balance before paid work.
  Track the total authorized cap across all operations, including cutouts and animation.
  Reserve an unresolved job's estimated charge until its canonical status resolves it.
- For image operations use `generate-or-edit-image`; for animation use
  `sprite-sheet-from-reference`, when installed. Both follow the bundled contract. If a task
  skill is absent, use the contract and actual public schemas instead of inventing fields.
- Save request, idempotency key, execution ID, and event cursor locally without credentials.
  Resume existing jobs after interruptions. Download to a new path and verify the file before
  marking an asset available. Never rerun generation to repair a download failure.

## Integrate and verify

Inspect each image. Check decoded format, dimensions, actual transparent pixels, visual
coherence, ground anchor/pivot, frame order, and per-frame timing. Prefer a reviewed still
frame when animation details drift; disclose the decision. Use the delivered timing array
when it differs from a rounded duration label, and record the discrepancy.

Keep collision and timing code independent of texture size. Add a baseline/artwork toggle
when useful for comparison. Validate both modes with the same deterministic input sequence,
then play a complete loop in the actual browser or engine. Test controls, pause/restart,
small screens, and reduced motion for decorative animation. For Godot/Unity use their
installed import skills; do not claim an engine was tested because its import files exist.

Record file digests, dimensions, upstream revision or generation execution ID, transformations,
historical costs separately from new charges, and any unverified behavior.

## Runnable example, no paid calls

The [Relay garden example](https://github.com/TheDesignFounder/dreamlayer-game-assets)
bundles DreamLayer robot frames and a geometry mode. With Node.js 22.19+ on the 22.x line (or another REA-supported version):

```sh
git clone https://github.com/TheDesignFounder/dreamlayer-game-assets.git
cd dreamlayer-game-assets
npm ci
npm test
npm run validate:assets
npm run art:plan
npm start
```

Open `http://127.0.0.1:4177/demo/`. No viewer key or credits are needed. Its plan script
submits nothing and defaults to a zero-credit cap. New generation uses the authenticated
canonical workflow above. The example's read-only recovery script never resubmits a job.

Only when the task actually needs artifact investigation, read
[the REA companion](references/rea-investigation.md). Ordinary game artwork does not require REA.
