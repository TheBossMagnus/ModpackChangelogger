import filecmp
import os
import subprocess
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # noqa # pylint disable=wrong-import-position

from modpack_changelogger.main import generate_changelog

old_pack = "test/packs/old.mrpack"
new_pack = "test/packs/new.mrpack"


def test_mr():
    expected_output = "test/expected/mr.md"

    generate_changelog(old_pack, new_pack, None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_cf():
    old_pack = "test/packs/old.zip"
    new_pack = "test/packs/new.zip"
    expected_output = "test/expected/cf.md"

    generate_changelog(old_pack, new_pack, None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

def test_formatted():
    expected_output = "test/expected/formatted.md"
    with open(expected_output, 'r') as file:
        expected_output = file.read()


    ret_changelog = generate_changelog(old_pack, new_pack, None, "formatted")
    if ret_changelog == expected_output:
        assert True
    else:
        assert False




def test_broken_config():
    config_path = "test/configs/broken_config.json"

    with pytest.raises(SystemExit):
        generate_changelog(old_pack, new_pack, config_path, None)


def test_run_as_script():
    script_name = "modpack_changelogger.py"
    expected_output = "test/expected/run_as_script.md"

    result = subprocess.run([sys.executable, script_name, "-o", old_pack, "-n", new_pack], check=False)

    assert result.returncode == 0
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

    if os.path.exists("Changelog.md"):
        os.remove("Changelog.md")
