using UnityEditor;
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
