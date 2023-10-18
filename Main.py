import json
import re
import sys
from Getmodname import GetModName

# Get the paths to old.json and new.json from command line arguments
if len(sys.argv) < 3:
    print("Usage: python Main.py <path_to_old_json> <path_to_new_json>")
    sys.exit(1)

old_json_path = sys.argv[1]
new_json_path = sys.argv[2]

# Load the old and new packs
with open(old_json_path, 'r', encoding="utf-8") as f:
    old_pack = json.load(f)
with open(new_json_path, 'r', encoding="utf-8") as f:
    new_pack = json.load(f)

# Get the Minecraft version from both packs
old_pack_mc_version = old_pack['dependencies']['minecraft']
new_pack_mc_version = new_pack['dependencies']['minecraft']

# Get the loader and his version from the index.json
old_pack_loader = list(old_pack['dependencies'].keys())[0]
old_pack_loader_version = old_pack['dependencies'][old_pack_loader]
new_pack_loader = list(new_pack['dependencies'].keys())[0]
new_pack_loader_version = new_pack['dependencies'][new_pack_loader]


# Load the list of mods from both packs
# Foreach Files entry in the json get the path key value
old_pack_urls = []
for file in old_pack['files']:
    old_pack_urls.append(file['downloads'])

new_pack_urls = []
for file in new_pack['files']:
    new_pack_urls.append(file['downloads'])

for NewMod in new_pack_urls.copy():
    for OldMod in old_pack_urls.copy():
        if NewMod == OldMod:
            old_pack_urls.remove(OldMod)
            new_pack_urls.remove(NewMod)



new_pack_ids = []
for url in new_pack_urls:
    new_pack_ids.append(re.search(r"(?<=data\/)[a-zA-Z0-9]{8}", str(url)).group(0))

old_pack_ids = []
for url in old_pack_urls:
    old_pack_ids.append(re.search(r"(?<=data\/)[a-zA-Z0-9]{8}", str(url)).group(0))

Updated_ids = []
New_ids = []
Removed_ids = []

for NewId in new_pack_ids.copy():
    for OldId in old_pack_ids.copy():
        if NewId == OldId:
            old_pack_ids.remove(OldId)
            new_pack_ids.remove(NewId)
            Updated_ids.append(NewId)

New_ids = new_pack_urls
Removed_ids = old_pack_urls
print(Removed_ids)

if len(Updated_ids) > 3:
    print("Updated mod:")
    for ModId in Updated_ids:
        print("- " + GetModName(ModId))

if len(New_ids) > 3:
    print("New mod:")
    for ModId in New_ids:
        print("- " + GetModName(ModId))

if len(Removed_ids) > 3:
    print("Removed mod:")
    for ModId in Removed_ids:
        print("- " + GetModName(ModId))
