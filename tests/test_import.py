import importlib.util, json, tempfile, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('importer',ROOT/'scripts/import_sprite.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
FIXTURE=ROOT/'examples/source/walk.zip'
class ImportTests(unittest.TestCase):
    def test_live_bundle_preserves_timing_and_alpha(self):
        frames,manifest=module.read_bundle(FIXTURE)
        self.assertEqual(len(frames),7)
        self.assertEqual(manifest['durations_ms'],[400,410,400,410,400,410,400])
        self.assertTrue(manifest['loop'])
    def test_both_engines_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            for engine in ('godot','unity'):
                dest=Path(tmp)/engine;module.build(FIXTURE,dest,engine)
                self.assertEqual(len(list(dest.rglob('*.png'))),7)
                with self.assertRaises(ValueError): module.build(FIXTURE,dest,engine)
    def test_rejects_traversal_and_bad_timing(self):
        with zipfile.ZipFile(FIXTURE) as z: original={n:z.read(n) for n in z.namelist()}
        for kind in ('traversal','timing'):
            with tempfile.TemporaryDirectory() as tmp:
                data=dict(original)
                if kind=='traversal': data['../bad.png']=b'x'
                else:
                    atlas=json.loads(data['atlas.json']);atlas['frame_durations_ms'][0]=0
                    data['atlas.json']=json.dumps(atlas).encode()
                path=Path(tmp)/'bad.zip'
                with zipfile.ZipFile(path,'w') as z:
                    for n,b in data.items():z.writestr(n,b)
                with self.assertRaises(ValueError): module.read_bundle(path)
if __name__=='__main__':unittest.main()
