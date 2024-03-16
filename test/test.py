import filecmp
import subprocess
import unittest
import sys
import os
sys.path.append(r'.\src')
from ModpackChangelogger import main

class TestModpackChangelogger(unittest.TestCase):
    def test_mr_packs(self):
            old_pack = r"test\packs\old1.mrpack"
            new_pack = r"test\packs\new1.mrpack"
            expected_output= r"test\expected\t1.md"

            main(old_pack, new_pack, None, None, False)
            self.assertTrue(filecmp.cmp('Changelog.md', expected_output, shallow=False))

    def test_cf_packs(self):
            old_pack = r"test\packs\old1.zip"
            new_pack = r"test\packs\new1.zip"
            expected_output= r"test\expected\t2.md"

            main(old_pack, new_pack, None, None, False)
            self.assertTrue(filecmp.cmp('Changelog.md', expected_output, shallow=False))

    def test_config_parameters(self):
        # Test different combinations of config parameters
        old_pack = r'test/packs/old1.mrpack'
        new_pack = r'test/packs/new1.mrpack'
        config_path = r'test/configs/config1.json'
        expected_output = r"test\expected\t3.md"
        main(old_pack, new_pack, config_path, None)
        self.assertTrue(filecmp.cmp('Changelog.md', expected_output, shallow=False))

    def test_config_parameters_2(self):
        # Test different combinations of config parameters
        old_pack = r'test/packs/old1.mrpack'
        new_pack = r'test/packs/new1.mrpack'
        config_path = r'test/configs/config2.json'
        expected_output = r"test\expected\t4.md"
        main(old_pack, new_pack, config_path, None)
        self.assertTrue(filecmp.cmp('Changelog.md', expected_output, shallow=False))

    def test_config_parameters_3(self):
        # Test different combinations of config parameters
        old_pack = r'test/packs/old1.mrpack'
        new_pack = r'test/packs/new1.mrpack'
        config_path = r'test/configs/config3.json'
        with self.assertRaises(SystemExit):
            main(old_pack, new_pack, config_path, None, False)


    def test_run_as_script(self):
        # Test running the script as a .py with parameters
        script_path = r'src/ModpackChangelogger.py'
        old_pack = r'test/packs/old1.mrpack'
        new_pack = r'test/packs/new1.mrpack'
        expected_output = r"test\expected\t5.md"

        # Run the script with subprocess.run()
        result = subprocess.run(
            ['python', script_path, '-o', old_pack, '-n', new_pack, '-f','name.md', '-d'],
        )

        self.assertEqual(result.returncode, 0)
        self.assertTrue(filecmp.cmp("name.md", expected_output, shallow=False))
        self.assertTrue(os.path.exists('config.json'))
        self.assertTrue(os.path.exists('log.txt'))

        #clenup
        os.remove('name.md')

if __name__ == '__main__':
    unittest.main()