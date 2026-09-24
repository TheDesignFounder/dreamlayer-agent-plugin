---
name: unity-sprite-import
description: "Prepare an existing DreamLayer sprite ZIP for Unity 2D with a local frame player and texture importer. Use when a Unity project needs the downloaded animation imported and played."
---

# unity sprite import

Read [the workflow contract](references/workflow-contract.md) for setup, billing, recovery and output checks.

This is local import and spends no credits. Use scripts/import_sprite.py with --engine unity --zip /absolute/walk.zip --out /absolute/new-demo. It generates an Assets/DreamLayerDemo folder, sprite import settings, a C# frame player with each frame's timing, and an Editor menu to create the demo. Copy Assets into a Unity project, wait for script compilation, then run Tools > DreamLayer > Create sprite demo and press Play. Do not overwrite existing assets without checking the destination. If the Unity editor is unavailable, mark compile/playback validation pending. This is an ordinary Unity import example, not a claim of inclusion in Unity's official plugin.

