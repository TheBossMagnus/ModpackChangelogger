import sys
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json

config = {}  # TBD: add a config file, using hardcoded values for now
config['format'] = "bullet"  # comma or bullet
config['check'] = {}
config['check']['added_mods'] = True
config['check']['removed_mods'] = True
config['check']['updated_mods'] = True
config['check']['loader'] = True
config['check']['mc_version'] = True
config['check']['config'] = True

# Get the paths to old.json and new.json from command line arguments and validate it
if len(sys.argv) < 3:
    print("Usage: python main.py <path_to_old_json> <path_to_new_json>")
    sys.exit(1)


# Parse the json files
old_json = get_json(sys.argv[1])
new_json = get_json(sys.argv[2])

# Compare the packs
added_mods, removed_mods, updated_mods = compare_packs(old_json, new_json, config)

#Print in a md doc
markdown_out(added_mods, removed_mods, updated_mods, config)