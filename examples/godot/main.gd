extends Node2D
var actor: AnimatedSprite2D
func _ready() -> void:
    var data = JSON.parse_string(FileAccess.get_file_as_string("res://frames/manifest.json"))
    var animation := SpriteFrames.new()
    animation.add_animation("dreamlayer")
    animation.set_animation_speed("dreamlayer", 1.0)
    animation.set_animation_loop("dreamlayer", data.loop)
    for i in range(data.frames.size()):
        var texture = load("res://frames/" + data.frames[i] + ".png")
        assert(texture != null, "Missing sprite texture")
        animation.add_frame("dreamlayer", texture, data.durations_ms[i] / 1000.0)
    actor = AnimatedSprite2D.new()
    actor.sprite_frames = animation
    actor.position = Vector2(320, 220)
    actor.scale = Vector2(2, 2)
    add_child(actor)
    actor.play("dreamlayer")
    if "--smoke" in OS.get_cmdline_user_args():
        var before := actor.frame
        await get_tree().create_timer(0.9).timeout
        assert(actor.is_playing(), "Animation stopped")
        assert(actor.frame != before, "Animation did not advance")
        print("DREAMLAYER_IMPORT_OK frames=", animation.get_frame_count("dreamlayer"))
        get_tree().quit()
