import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from modpack_changelogger import generate_changelog

old_pack = r"D:\ModpackChangelogger/test/packs/old.mrpack"
new_pack = r"D:\ModpackChangelogger/test/packs/new.mrpack"
name = None

json_path = os.path.join(r"D:\ModpackChangelogger\test\configs", f"{name}.json")
if not os.path.isfile(json_path):
    json_path = None
md_path = os.path.join(r"D:\ModpackChangelogger\test\expected", f"{name}.md")

generate_changelog(old_pack, new_pack, json_path, md_path)
