import sys
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json

# Get the paths to old.json and new.json from command line arguments and validate it
if len(sys.argv) < 3:
    print("Usage: python main.py <path_to_old_json> <path_to_new_json>")
    sys.exit(1)

# Parse the json files
old_json = get_json(sys.argv[1])
new_json = get_json(sys.argv[2])

# Compare the packs
added_mods, removed_mods, updated_mods = compare_packs(old_json, new_json)

#Print in a md doc
markdown_out(added_mods, removed_mods, updated_mods)