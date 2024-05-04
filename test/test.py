import filecmp
import os
import subprocess
import sys
import pytest

from modpack_changelogger.main import generate_changelog

def test_mr_packs():
    old_pack = "test/packs/old.mrpack"
    new_pack = "test/packs/new.mrpack"
    expected_output = "test/expected/t1.md"

    generate_changelog(old_pack, new_pack, None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

def test_cf_packs():
    old_pack = "test/packs/old.zip"
    new_pack = "test/packs/new.zip"
    expected_output = "test/expected/t2.md"

    generate_changelog(old_pack, new_pack, None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

def test_config_parameters():
    old_pack = "test/packs/old.mrpack"
    new_pack = "test/packs/new.mrpack"
    config_path = "test/configs/config1.json"
    expected_output = "test/expected/t3.md"

    generate_changelog(old_pack, new_pack, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

def test_config_parameters_2():
    old_pack = "test/packs/old.mrpack"
    new_pack = "test/packs/new.mrpack"
    config_path = "test/configs/config2.json"
    expected_output = "test/expected/t4.md"

    generate_changelog(old_pack, new_pack, config_path, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

def test_config_parameters_3():
    old_pack = "test/packs/old.mrpack"
    new_pack = "test/packs/new.mrpack"
    config_path = "test/configs/config3.json"

    with pytest.raises(SystemExit):
        generate_changelog(old_pack, new_pack, config_path, None, False)

def test_run_as_script():
    script_path = r"modpack_changelogger.py"
    old_pack = "test/packs/old.mrpack"
    new_pack = "test/packs/new.mrpack"
    expected_output = "test/expected/t5.md"

    result = subprocess.run([sys.executable, script_path, "-o", old_pack, "-n", new_pack, "-f", "name.md", "-c", "new", "-d"], check=False)

    assert result.returncode == 0
    assert filecmp.cmp("name.md", expected_output, shallow=False)
    assert os.path.exists("config.json")
    assert os.path.exists("log.txt")

    for file in ["Changelog.md", "config.json", "log.txt", "name.md"]:
        if os.path.exists(file):
            os.remove(file)