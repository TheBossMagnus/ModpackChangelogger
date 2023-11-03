import sys
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json
from config_handler import load_config, create_config


if sys.argv[1] == "config":
    if sys.argv[2] == "reset":
        create_config()
        sys.exit(0)
elif len(sys.argv) != 3:
    print("ERROR: arguments must be \"python main.py <path_to_old_json> <path_to_new_json>\"")
    sys.exit(1)

config=load_config()

# Parse the json files
old_json = get_json(sys.argv[1])
new_json = get_json(sys.argv[2])

# Compare the packs
added_mods, removed_mods, updated_mods = compare_packs(old_json, new_json, config)

#Print in a md doc
markdown_out(added_mods, removed_mods, updated_mods, config)