import json
import re

# Load the old and new packs
with open('old.json', 'r') as f:
    old_pack = json.load(f)
with open('new.json', 'r') as f:
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
old_pack_mods = []
for file in old_pack['files']:
    old_pack_mods.append(file['path'])

new_pack_mods = []
for file in new_pack['files']:
    new_pack_mods.append(file['path'])

# Create arrays for the added, updated and removed mods
added_mods = []
updated_mods = []
removed_mods = []

# Detect updated, added and removed mods
for new_mod in new_pack_mods:
    found = False
    for old_mod in old_pack_mods:
        if new_mod == old_mod:
            found = True
            old_pack_mods.remove(old_mod)
            break
        elif (re.sub('[\d\.]+|\+.*|jar|-alpha|-beta', '', new_mod) ==
              re.sub('[\d\.]+|\+.*|jar|-alpha|-beta', '', old_mod)):
            found = True
            updated_mods.append(new_mod)
            old_pack_mods.remove(old_mod)
            break
    if not found:
        added_mods.append(new_mod)
removed_mods = old_pack_mods

# Write the changelog
with open('Changelog.md', 'w') as f:
    f.write('')

if len(added_mods) > 0:
    with open('Changelog.md', 'a') as f:
        f.write('### Added:\n')
        for mod in added_mods:
            f.write(f'- {mod}\n')

if len(updated_mods) > 0:
    with open('Changelog.md', 'a') as f:
        f.write('### Updated:\n')
        for mod in updated_mods:
            f.write(f'- {mod}\n')

if len(removed_mods) > 0:
    with open('Changelog.md', 'a') as f:
        f.write('### Removed:\n')
        for mod in removed_mods:
            f.write(f'- {mod}\n')