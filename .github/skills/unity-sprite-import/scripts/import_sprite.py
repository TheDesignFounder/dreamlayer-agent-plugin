"""Import a DreamLayer ZIP into a new Godot/Unity example. No API calls or dependencies."""
import argparse, json, math, re, struct, zipfile
from pathlib import Path, PurePosixPath

GODOT_SCRIPT = '''extends Node2D
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
'''

UNITY_PLAYER = '''using System;
using UnityEngine;
[RequireComponent(typeof(SpriteRenderer))]
public class DreamLayerFramePlayer : MonoBehaviour {
    [Serializable] public class Manifest {
        public string[] frames;
        public float[] durations_ms;
        public bool loop;
    }
    private Sprite[] frames;
    private Manifest manifest;
    private SpriteRenderer target;
    private int index;
    private float elapsed;
    private bool finished;
    void Start() {
        var text = Resources.Load<TextAsset>("DreamLayerDemo/manifest");
        if (text == null) { Debug.LogError("Missing DreamLayer manifest"); enabled=false; return; }
        manifest = JsonUtility.FromJson<Manifest>(text.text);
        if (manifest.frames == null || manifest.frames.Length == 0 || manifest.durations_ms == null || manifest.frames.Length != manifest.durations_ms.Length) {
            Debug.LogError("Invalid DreamLayer timing manifest"); enabled=false; return;
        }
        target = GetComponent<SpriteRenderer>();
        frames = new Sprite[manifest.frames.Length];
        for(int i=0;i<frames.Length;i++) {
            frames[i]=Resources.Load<Sprite>("DreamLayerDemo/"+manifest.frames[i]);
            if(frames[i]==null || manifest.durations_ms[i]<=0) { Debug.LogError("Invalid DreamLayer frame"); enabled=false; return; }
        }
        target.sprite=frames[0];
    }
    void Update() {
        if(finished || frames==null) return;
        elapsed+=Time.deltaTime;
        while(elapsed>=manifest.durations_ms[index]/1000f) {
            elapsed-=manifest.durations_ms[index]/1000f;
            if(index==frames.Length-1 && !manifest.loop) { finished=true; return; }
            index=(index+1)%frames.Length;
            target.sprite=frames[index];
        }
    }
}
'''

UNITY_EDITOR = '''using UnityEditor;
using UnityEngine;
public class DreamLayerSpriteImporter : AssetPostprocessor {
    void OnPreprocessTexture() {
        if(!assetPath.StartsWith("Assets/DreamLayerDemo/Resources/DreamLayerDemo/")) return;
        var importer=(TextureImporter)assetImporter;
        importer.textureType=TextureImporterType.Sprite;
        importer.spriteImportMode=SpriteImportMode.Single;
        importer.spritePixelsPerUnit=128;
        importer.alphaIsTransparency=true;
        importer.mipmapEnabled=false;
        importer.textureCompression=TextureImporterCompression.Uncompressed;
    }
    [MenuItem("Tools/DreamLayer/Create sprite demo")]
    public static void CreateDemo() {
        var actor=new GameObject("DreamLayer sprite demo");
        Undo.RegisterCreatedObjectUndo(actor,"Create DreamLayer demo");
        actor.AddComponent<SpriteRenderer>();
        actor.AddComponent<DreamLayerFramePlayer>();
        if(Camera.main==null) {
            var cameraObject=new GameObject("DreamLayer demo camera");
            Undo.RegisterCreatedObjectUndo(cameraObject,"Create DreamLayer camera");
            cameraObject.tag="MainCamera";
            var camera=cameraObject.AddComponent<Camera>();
            camera.orthographic=true; camera.orthographicSize=1.5f;
            cameraObject.transform.position=new Vector3(0,0,-10);
        }
        Selection.activeGameObject=actor;
    }
}
'''

def read_bundle(path):
    with zipfile.ZipFile(path) as z:
        infos=z.infolist()
        if len(infos)>150 or sum(i.file_size for i in infos)>200*1024*1024:
            raise ValueError('Bundle exceeds import limits')
        names=[i.filename for i in infos]
        if len(set(names))!=len(names): raise ValueError('Duplicate ZIP entries')
        for name in names:
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or '\\' in name:
                raise ValueError('Unsafe ZIP path')
        atlas=json.loads(z.read('atlas.json'))
        if atlas.get('schema_version')!=1: raise ValueError('Unsupported atlas schema')
        order=list(atlas['frames'])
        if not 7<=len(order)<=100 or atlas['frame_count']!=len(order):
            raise ValueError('Frame count mismatch')
        durations=atlas.get('frame_durations_ms')
        if not isinstance(durations,list) or len(durations)!=len(order):
            raise ValueError('Missing per-frame durations')
        if any(type(t) not in (int,float) or not math.isfinite(t) or t<=0 for t in durations):
            raise ValueError('Invalid duration')
        frames={}
        for name in order:
            if not re.fullmatch(r'[A-Za-z0-9_-]+',name): raise ValueError('Unsafe frame name')
            data=z.read('frames/'+name+'.png')
            if len(data)<33 or data[:8]!=b'\x89PNG\r\n\x1a\n': raise ValueError('Invalid PNG')
            width,height=struct.unpack('>II',data[16:24])
            if width!=atlas['cell'] or height!=atlas['cell']: raise ValueError('Canvas mismatch')
            if data[25] not in (4,6): raise ValueError('PNG lacks an alpha channel')
            frames[name]=data
        manifest={'frames':order,'durations_ms':durations,
                  'loop':atlas.get('animation_mode','loop' if atlas.get('action') in ('walk','run','idle') else 'once')=='loop',
                  'width':atlas['cell'],'height':atlas['cell']}
        return frames,manifest

def build(bundle,out,engine):
    frames,manifest=read_bundle(bundle)
    out=Path(out)
    if out.exists(): raise ValueError('Destination must be new; refusing overwrite')
    out.mkdir(parents=True)
    assets=out/'frames' if engine=='godot' else out/'Assets/DreamLayerDemo/Resources/DreamLayerDemo'
    assets.mkdir(parents=True)
    for name,data in frames.items(): (assets/(name+'.png')).write_bytes(data)
    (assets/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if engine=='godot':
        (out/'project.godot').write_text('config_version=5\n[application]\nconfig/name="DreamLayer sprite demo"\nrun/main_scene="res://main.tscn"\n[display]\nwindow/size/viewport_width=640\nwindow/size/viewport_height=440\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
        (out/'main.tscn').write_text('[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://main.gd" id="1"]\n[node name="DreamLayerDemo" type="Node2D"]\nscript = ExtResource("1")\n')
        (out/'main.gd').write_text(GODOT_SCRIPT)
        (out/'.gitignore').write_text('.godot/\n')
    else:
        base=out/'Assets/DreamLayerDemo'
        (base/'Editor').mkdir()
        (base/'DreamLayerFramePlayer.cs').write_text(UNITY_PLAYER)
        (base/'Editor/DreamLayerSpriteImporter.cs').write_text(UNITY_EDITOR)
    print(json.dumps({'engine':engine,'frames':len(frames),'duration_ms':sum(manifest['durations_ms']),'output':str(out)}))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',choices=['godot','unity'],required=True)
    p.add_argument('--zip',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();build(a.zip,a.out,a.engine)
