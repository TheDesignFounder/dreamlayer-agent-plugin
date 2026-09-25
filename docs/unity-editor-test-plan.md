# Unity editor test plan

Godot import is validated end to end. Unity is not: this repository ships importer code
and instructions, and no Unity editor run has been completed. Until someone executes the
steps below, do not describe Unity as validated anywhere.

## Why it is not validated here

Unity Hub and the Unity Editor are not installed on the machine used for distribution
work, and installing a multi-gigabyte editor, creating a Unity account or accepting a
licence were all out of scope. Everything that can be checked without the editor has been
checked; see "Static checks already passing" below.

## Required environment

- Unity 6.0 LTS or newer, 2D template. The sample uses only `SpriteRenderer`,
  `Texture2D`, `Resources.Load`, `TextureImporter` and `AssetPostprocessor`, which are
  stable across recent versions, so any modern 2D-capable editor should work. Record the
  exact version you use.
- Unity Hub, a signed-in Unity account and a personal licence.
- Python 3 for the importer script.

## Steps

1. Generate a fresh project folder from a real bundle, which spends no credits:

   ```sh
   python3 scripts/import_sprite.py --engine unity --zip examples/source/walk.zip --out /absolute/new-unity-demo
   ```

   The destination must not already exist. Expect
   `{"engine": "unity", "frames": 7, "duration_ms": 2830, ...}`.

2. Create a new 2D project in Unity Hub, then copy
   `/absolute/new-unity-demo/Assets/DreamLayerDemo` into the project's `Assets/`.

3. Let scripts compile. The console must show no compiler errors.

4. Choose **Tools > DreamLayer > Create sprite demo**. It creates a GameObject with a
   `SpriteRenderer` and the `DreamLayerFramePlayer` component.

5. Press Play.

## What must be true

- Seven sprites load from `Resources/DreamLayerDemo`, named `walk_01` to `walk_07`.
- Each is 128x128 with a real alpha channel, imported as a Sprite with
  `alphaIsTransparency` set and no compression.
- The player advances frames on the manifest's own durations: 400, 410, 400, 410, 400,
  410, 400 milliseconds, a 2.83-second cycle.
- The animation loops, because the manifest sets `loop: true`.
- No console errors or warnings from the DreamLayer scripts during Play.

## Static checks already passing

Run without any editor, on 2026-09-25, from a fresh importer run:

- The importer produced the documented layout: `DreamLayerFramePlayer.cs`,
  `Editor/DreamLayerSpriteImporter.cs`, `Resources/DreamLayerDemo/manifest.json` and seven
  PNG frames.
- Every frame is PNG colour type 6, that is RGBA, at 128x128, matching `width` and
  `height` in the manifest.
- The manifest's `frames` list matches the files on disk one for one, and
  `durations_ms` has one entry per frame summing to 2830.
- The generated scripts expose `Tools/DreamLayer/Create sprite demo`, load
  `DreamLayerDemo/manifest` through `Resources`, and set `TextureImporterType.Sprite`
  with `alphaIsTransparency`.

What these do not establish: that the project compiles under a specific Unity version,
that Play mode runs, or that the animation looks correct in the editor. Those are exactly
what the steps above exist to settle.

## After a successful run

Record the Unity version, the console result and the observed cycle in
`research/`, then update the Unity wording in `README.md`, the ClawHub listing and
`docs/hermes-setup.md` in the same change. Until then they all say editor validation is
not confirmed.
