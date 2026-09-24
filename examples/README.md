# Reference to animation

`source/reference.png` and `source/walk.zip` were generated through the public DreamLayer Agent API. The example uses seven 128×128 frames at 5.8 sprite credits, plus one credit for the original reference.

## Godot
Open `godot/project.godot` in Godot 4. The scene plays the delivered per-frame timing.
```sh
godot --headless --path examples/godot --editor --quit
godot --headless --path examples/godot -- --smoke
```
Validated with Godot 4.7.2. For a full-cycle check on a **fresh import**:

```sh
python3 scripts/import_sprite.py --engine godot --zip examples/source/walk.zip --out /tmp/dreamlayer-godot-check
godot --headless --editor --path /tmp/dreamlayer-godot-check --quit
godot --headless --path /tmp/dreamlayer-godot-check --script "$PWD/scripts/validate_godot.gd"
```

The validator checks seven frame textures, dimensions, transparent pixels,
per-frame durations, animation advancement, and looping. It exits nonzero on
failure or after a 30-second watchdog timeout; use it with short example clips.
For the included ZIP it verifies a 2.83-second cycle. Engine source APIs were
also inspected in Godot 4.8-dev; that source build has **not** been compiled or
runtime-tested. No engine-source checkout is required to import the assets.

## Unity
Copy `unity/Assets/DreamLayerDemo` into a new Unity 2D project. After scripts compile, choose **Tools > DreamLayer > Create sprite demo**, then press Play. The player preserves each frame's duration. Unity compilation/playback is pending; these files are not a verified Unity release.

## Your bundle
```sh
python3 scripts/import_sprite.py --engine godot --zip /absolute/walk.zip --out /absolute/new-godot-demo
python3 scripts/import_sprite.py --engine unity --zip /absolute/walk.zip --out /absolute/new-unity-demo
```
Destinations must not already exist. The importer validates the bundle before writing and does not call the API.

Review motion before using it: the sample's robot eye and body details vary across frames. Import correctness and generated animation quality are separate checks.
