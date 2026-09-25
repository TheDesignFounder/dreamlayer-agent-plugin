---
name: godot-sprite-import
description: "Import an existing DreamLayer sprite ZIP into a Godot 4 demo and play the animation. Use when the user already has generated frames and wants a runnable game-engine example."
---

# godot sprite import

Read [the workflow contract](references/workflow-contract.md) for setup, billing, recovery and output checks.

This is local import and spends no credits. Use scripts/import_sprite.py with --engine godot --zip /absolute/walk.zip --out /absolute/new-demo. It reads PNG frames and atlas durations from the bundle, validates them and creates a Godot 4 project with AnimatedSprite2D. Run godot --headless --path /absolute/new-demo --editor --quit, then open the project and inspect playback. Preserve returned frame durations; do not assume constant FPS. Use the generated demo as a reference when importing into an existing project, keeping existing settings intact. If Godot is unavailable, mark engine validation pending; successful file generation alone does not prove engine playback.

