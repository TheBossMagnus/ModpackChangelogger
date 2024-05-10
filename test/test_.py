import filecmp
import io
import os
import re
import subprocess
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modpack_changelogger.main import generate_changelog  # pylint:disable=C0413

OLD_PACK = "test/packs/old.mrpack"
NEW_PACK = "test/packs/new.mrpack"


def test_mr():
    expected_output = "test/expected/mr.md"

    generate_changelog(OLD_PACK, NEW_PACK, None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_cf():
    expected_output = "test/expected/cf.md"

    generate_changelog("test/packs/old.zip", "test/packs/new.zip", None, None)
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)


def test_formatted():
    expected_output = "test/expected/formatted.md"
    with open(expected_output, "r", encoding="utf-8") as file:
        expected_output = file.read()

    assert expected_output == generate_changelog(OLD_PACK, NEW_PACK, None, "formatted")


def test_unformatted():
    expected_output_file = "test/expected/unformatted.md"

    output1, output2, output3 = generate_changelog(OLD_PACK, NEW_PACK, None, "unformatted")

    with open(expected_output_file, "r", encoding="utf-8") as f:
        expected1, expected2, expected3 = f.read().split("\n")

    assert str(output1) == expected1.strip()
    assert str(output2) == expected2.strip()
    assert str(output3) == expected3.strip()


def test_console():
    expected_output_file = "test/expected/console.md"

    console_output = io.StringIO()
    sys.stdout = console_output
    generate_changelog(OLD_PACK, NEW_PACK, None, "console")
    sys.stdout = sys.__stdout__
    console_output = console_output.getvalue()

    with open(expected_output_file, "r", encoding="utf-8") as file:
        expected_output = file.read()

    assert expected_output == console_output


def test_config_new():
    generate_changelog(None, None, "new", None)
    try:
        assert os.path.isfile("config.json")
    finally:
        os.remove("config.json")


def test_version():
    script_name = "modpack_changelogger.py"

    result = subprocess.run([sys.executable, script_name, "-v"], check=False, capture_output=True, text=True)
    assert re.fullmatch(r"ModpackChangelogger \d+\.\d+\.\d+(-\w+)?", result.stdout.strip()) is not None

    assert result.returncode == 0


def test_broken_config():
    config_path = "test/configs/broken_config.json"

    with pytest.raises(SystemExit):
        generate_changelog(OLD_PACK, NEW_PACK, config_path, None)


def test_run_as_script():
    script_name = "modpack_changelogger.py"
    expected_output = "test/expected/run_as_script.md"

    result = subprocess.run([sys.executable, script_name, "-o", OLD_PACK, "-n", NEW_PACK], check=False)

    assert result.returncode == 0
    assert filecmp.cmp("Changelog.md", expected_output, shallow=False)

    if os.path.exists("Changelog.md"):
        os.remove("Changelog.md")
