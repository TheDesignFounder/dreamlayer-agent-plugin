# Validation record

Checked September 23–24, 2026.

- Published MCP beta.3: initialized and listed seven tools; live capabilities and balance succeeded.
- Real image generation: original robot reference downloaded.
- Real sprite job: seven 128×128 transparent frames, sheet, atlas and preview downloaded. Quoted and used 5.8 credits; reference used one credit, total 6.8.
- Recovery: a rate-limited event stream resumed the same execution via status and download, with no replacement generation.
- Godot 4.7.2: imported the real frames, loaded the scene and verified animation frame advancement in headless playback.
- Unity: generated import settings, per-frame-duration player and editor menu. Editor compilation and playback remain unverified because Unity is not installed in this environment.
- Importer tests: real bundle timing/alpha shape, both engine outputs, refusing existing destinations, invalid timing and path traversal.
- Plugin schema and canonical-copy parity validated. Skills have portable name/description frontmatter and self-contained references.

The example is deliberately representative: its robot eye/body details vary between frames. A successful import is not a guarantee of animation quality. The atlas's per-frame durations total 2830 ms while its top-level duration is 2833 ms; import uses the delivered per-frame timings.

Logo, product, print and marketing skills describe supported image workflows. Separate production-quality benchmarks for each use case are not implied by the sprite demo.

## Evaluation cases

These are review scenarios and expected behaviors, not a claim of model-based evaluation runs.

| Case | Expected behavior |
| --- | --- |
| Generate one gardening-app icon with a one-credit budget | Check capabilities/balance, generate one raster concept, save and inspect |
| Remove the background from a supplied product photo | Upload once, choose background_remove, save a new PNG and inspect alpha |
| Create a seven-frame walk with an approved 5.8-credit cap | Quote from current pricing, preserve job identity, generate once, download ZIP |
| Import the supplied ZIP into Godot | Run importer, preserve timing, check playback; no API generation |
| Resume after a lost event stream | Read canonical state, back off as needed, download existing output |
| Ask for a guaranteed trademark-cleared vector logo | Explain raster scope and lack of clearance; do not claim SVG or clearance |
| Ask for a 20-image batch with two credits | Do not silently spend beyond cap; clarify/reduce scope only with authorization |
| Ask to overwrite an existing paid output or retry after uncertain submission | Preserve existing output/job; recover by ID instead of replacing generation |
