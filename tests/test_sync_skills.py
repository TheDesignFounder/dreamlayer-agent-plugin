import importlib.util, shutil, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync_skills',ROOT/'scripts/sync_skills.py')
sync_skills=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync_skills)

def build(root):
    """A miniature repository: one plain skill and one that carries the import script."""
    (root/'docs').mkdir(parents=True);(root/'docs/workflow-contract.md').write_text('contract v1\n')
    (root/'scripts').mkdir();(root/'scripts/import_sprite.py').write_text('# importer v1\n')
    for name in ('demo-skill','godot-sprite-import'):
        folder=root/sync_skills.CANONICAL/name;folder.mkdir(parents=True)
        (folder/'SKILL.md').write_text(f'---\nname: {name}\ndescription: Demo.\n---\n\nBody.\n')
    return root

class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=build(Path(self.tmp.name))

    def mirrors(self):
        return [self.root/mirror for mirror in sync_skills.MIRRORS]

    def test_generates_every_host_path_then_reports_clean(self):
        self.assertTrue(sync_skills.sync(self.root,check=True))
        for mirror in self.mirrors(): self.assertFalse(mirror.exists())
        sync_skills.sync(self.root)
        self.assertEqual(sync_skills.sync(self.root,check=True),[])
        for mirror in self.mirrors():
            self.assertEqual((mirror/'demo-skill/SKILL.md').read_text(),
                             (self.root/sync_skills.CANONICAL/'demo-skill/SKILL.md').read_text())
            self.assertEqual((mirror/'godot-sprite-import/scripts/import_sprite.py').read_text(),'# importer v1\n')
            self.assertEqual((mirror/'demo-skill/references/workflow-contract.md').read_text(),'contract v1\n')
            self.assertFalse((mirror/'demo-skill/scripts/import_sprite.py').exists())
            self.assertIn(sync_skills.CANONICAL,(mirror/'README.md').read_text())

    def test_check_finds_edited_copy_and_rewrite_restores_it(self):
        sync_skills.sync(self.root)
        edited=self.root/'.cline/skills/demo-skill/SKILL.md'
        edited.write_text('---\nname: demo-skill\ndescription: Forked.\n---\n')
        problems=sync_skills.sync(self.root,check=True)
        self.assertEqual(len(problems),1)
        self.assertIn('.cline/skills/demo-skill/SKILL.md',problems[0])
        self.assertIn('differs',problems[0])
        self.assertEqual(edited.read_text(),'---\nname: demo-skill\ndescription: Forked.\n---\n')
        sync_skills.sync(self.root)
        self.assertIn('Body.',edited.read_text())
        self.assertEqual(sync_skills.sync(self.root,check=True),[])

    def test_check_finds_extra_file_and_rewrite_removes_it(self):
        sync_skills.sync(self.root)
        stray=self.root/'.github/skills/demo-skill/EXTRA.md'
        stray.write_text('not canonical\n')
        problems=sync_skills.sync(self.root,check=True)
        self.assertEqual([p for p in problems if 'EXTRA.md' in p and 'not in the canonical source' in p],problems)
        sync_skills.sync(self.root)
        self.assertFalse(stray.exists())

    def test_vendored_file_change_reaches_every_copy(self):
        sync_skills.sync(self.root)
        (self.root/'docs/workflow-contract.md').write_text('contract v2\n')
        self.assertTrue(any('stale copy' in p for p in sync_skills.sync(self.root,check=True)))
        sync_skills.sync(self.root)
        for mirror in self.mirrors():
            self.assertEqual((mirror/'demo-skill/references/workflow-contract.md').read_text(),'contract v2\n')
        self.assertEqual(sync_skills.sync(self.root,check=True),[])

    def test_editor_leftovers_are_not_drift(self):
        sync_skills.sync(self.root)
        (self.root/'.agents/skills/demo-skill/.DS_Store').write_bytes(b'\x00')
        cache=self.root/'.agents/skills/demo-skill/__pycache__';cache.mkdir()
        (cache/'x.pyc').write_bytes(b'\x00')
        self.assertEqual(sync_skills.sync(self.root,check=True),[])

    def test_canonical_source_is_never_rewritten_from_a_mirror(self):
        sync_skills.sync(self.root)
        canonical=self.root/sync_skills.CANONICAL/'demo-skill/SKILL.md'
        before=canonical.read_bytes()
        shutil.rmtree(self.root/'.cline/skills/demo-skill')
        (self.root/'.github/skills/demo-skill/SKILL.md').write_text('forked\n')
        sync_skills.sync(self.root)
        self.assertEqual(canonical.read_bytes(),before)
        self.assertEqual((self.root/'.github/skills/demo-skill/SKILL.md').read_bytes(),before)
        self.assertTrue((self.root/'.cline/skills/demo-skill/SKILL.md').exists())

if __name__=='__main__': unittest.main()
