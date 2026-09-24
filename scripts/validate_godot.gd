# Run against a fresh import: godot --headless --path PROJECT --script /absolute/path/validate_godot.gd
extends SceneTree

var failures: Array[String] = []
var frame_changes := 0
var loops := 0
var finished := false

func check(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
        push_error(message)

func _initialize() -> void:
    watchdog.call_deferred()
    run.call_deferred()

func watchdog() -> void:
    await create_timer(30.0).timeout
    push_error("Validation exceeded 30 seconds")
    quit(1)

func run() -> void:
    var packed = load("res://main.tscn")
    if packed == null:
        push_error("Missing imported main scene")
        quit(1)
        return
    var scene = packed.instantiate()
    root.add_child(scene)
    await process_frame
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://frames/manifest.json"))
    var actor: AnimatedSprite2D = scene.get("actor") as AnimatedSprite2D
    if actor == null or not manifest is Dictionary:
        push_error("Missing actor or manifest")
        quit(1)
        return
    var frames: SpriteFrames = actor.sprite_frames
    check(frames.get_frame_count("dreamlayer") == manifest.frames.size(), "Frame count mismatch")
    check(is_equal_approx(frames.get_animation_speed("dreamlayer"), 1.0), "Timing expects 1 FPS base")
    check(frames.get_animation_loop("dreamlayer") == manifest.loop, "Loop flag mismatch")
    var duration := 0.0
    for i in range(manifest.frames.size()):
        var seconds: float = manifest.durations_ms[i] / 1000.0
        duration += seconds
        check(is_equal_approx(frames.get_frame_duration("dreamlayer", i), seconds), "Frame duration mismatch")
        var texture: Texture2D = frames.get_frame_texture("dreamlayer", i)
        check(texture != null, "Missing texture")
        if texture != null:
            check(texture.get_width() == manifest.width and texture.get_height() == manifest.height, "Frame dimensions mismatch")
            var image: Image = texture.get_image()
            check(image != null and image.detect_alpha() != Image.ALPHA_NONE, "Missing transparent pixels")
    actor.frame_changed.connect(func(): frame_changes += 1)
    actor.animation_looped.connect(func(): loops += 1)
    actor.animation_finished.connect(func(): finished = true)
    # Full cycle verifies loop/end behavior; checking a single frame after a fixed
    # delay can accidentally inspect the same frame on a healthy looping sprite.
    actor.stop()
    actor.play("dreamlayer")
    await create_timer(duration + 0.35).timeout
    if manifest.frames.size() > 1:
        check(frame_changes > 0, "Animation never advanced")
    if manifest.loop:
        check(loops >= 1 and actor.is_playing(), "Animation did not loop")
    else:
        check(finished and not actor.is_playing(), "Animation did not finish")
    if failures.is_empty():
        print("DREAMLAYER_VALIDATED frames=", manifest.frames.size(), " dimensions=", manifest.width, "x", manifest.height, " cycle_seconds=", duration, " loops=", loops, " frame_changes=", frame_changes)
    quit(0 if failures.is_empty() else 1)
