import filecmp
# import subprocess
import unittest
import sys
sys.path.append('.\src')
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

''' WIP
    def test_config_parameters(self):
        # Test different combinations of config parameters
        old_pack = 'tests/old.mrpack'
        new_pack = 'tests/new.mrpack'
        config_path = 'tests/config1.json'
        expected_output = '...'  # Replace with the expected output
        output = main(old_pack, new_pack, config_path, None)
        self.assertEqual(output, expected_output)

    def test_run_as_script(self):
        # Test running the script as a .py with parameters
        script_path = 'ModpackChangelogger.py'
        old_pack = 'tests/old.mrpack'
        new_pack = 'tests/new.mrpack'
        config_path = 'tests/config.json'
        expected_output = '...'  # Replace with the expected output

        # Run the script with subprocess.run()
        result = subprocess.run(
            ['python', script_path, old_pack, new_pack, config_path],
            text=True,
            capture_output=True,
        )

        # Check the script's output
        self.assertEqual(result.stdout, expected_output)

'''
if __name__ == '__main__':
    unittest.main()