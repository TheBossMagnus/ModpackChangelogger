import json
import re
import sys
import asyncio
from Getmodname import GetModName

# Get the paths to old.json and new.json from command line arguments
if len(sys.argv) < 3:
    print("Usage: python Main.py <path_to_old_json> <path_to_new_json>")
    sys.exit(1)

oldJsonPath = sys.argv[1]
newJsonPath = sys.argv[2]

# Load the old and new packs
with open(oldJsonPath, 'r', encoding="utf-8") as f:
    oldPack = json.load(f)
with open(newJsonPath, 'r', encoding="utf-8") as f:
    newPack = json.load(f)

# Get the Minecraft version from both packs
oldPackMcVersion = oldPack['dependencies']['minecraft']
newPackMcVersion = newPack['dependencies']['minecraft']

# Get the loader and his version from the index.json
oldPackLoader = list(oldPack['dependencies'].keys())[0]
oldPackLoaderVersion = oldPack['dependencies'][oldPackLoader]
newPackLoader = list(newPack['dependencies'].keys())[0]
newPackLoaderVersion = newPack['dependencies'][newPackLoader]


# Load the list of mods from both packs
# Foreach Files entry in the json get the path key value
oldPackUrls = []
for file in oldPack['files']:
    oldPackUrls.append(file['downloads'])

newPackUrls = []
for file in newPack['files']:
    newPackUrls.append(file['downloads'])


# If an url is in both packs its untached, so ignore it
for newMod in newPackUrls.copy():
    for oldMod in oldPackUrls.copy():
        if newMod == oldMod:
            oldPackUrls.remove(oldMod)
            newPackUrls.remove(newMod)



newPackIds = []
for url in newPackUrls:
    newPackIds.append(re.search(r"(?<=data\/)[a-zA-Z0-9]{8}", str(url)).group(0))

oldPackIds = []
for url in oldPackUrls:
    oldPackIds.append(re.search(r"(?<=data\/)[a-zA-Z0-9]{8}", str(url)).group(0))

updatedIds = []
newIds = []
removedIds = []

# If an id is in both packs its updated, add it to the updated list
for newId in newPackIds.copy():
    for oldId in oldPackIds.copy():
        if newId == oldId:
            oldPackIds.remove(oldId)
            newPackIds.remove(newId)
            updatedIds.append(newId)

newIds = newPackIds
removedIds = oldPackIds

async def main():
    if updatedIds:
        print("Updated mod:")
        print("\n".join(["- " + name for name in await asyncio.gather(*[GetModName(ModId) for ModId in updatedIds])]))

    if newIds:
        print("New mod:")
        print("\n".join(["- " + name for name in await asyncio.gather(*[GetModName(ModId) for ModId in newIds])]))

    if removedIds:
        print("Removed mod:")
        print("\n".join(["- " + name for name in await asyncio.gather(*[GetModName(ModId) for ModId in removedIds])]))

asyncio.run(main())