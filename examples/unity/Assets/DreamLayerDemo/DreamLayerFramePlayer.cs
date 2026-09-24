using System;
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
