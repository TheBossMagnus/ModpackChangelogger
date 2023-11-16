import sys
import asyncio
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json
from config_handler import load_config, create_config

def main(old_path, new_path):
    config = load_config()

    # Parse the json files
    old_json = get_json(old_path)
    new_json = get_json(new_path)

    # Compare the packs
    added, removed, updated = asyncio.run(compare_packs(old_json, new_json, config))

    # Print in a md doc
    markdown_out(added, removed, updated, config)

if __name__ == "__main__":
    if sys.argv[1] == "-cc" or sys.argv[1] == "--create-config":
        create_config()
    elif (sys.argv[1] == "-o" or sys.argv[1] == "--old") and (sys.argv[3] == "-n" or sys.argv[3] == "--new"):
        main(sys.argv[2], sys.argv[4])
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "-?":
        print("Usage:")
        print("  -o, --old                   The pack to compare to")
        print("  -n, --new                   The pack to compare")
        print("  -cc, --create-config        Create a config file")
        print("  -h, --help                  show this help message and exit")
    else:
        print("Error: Invalid arguments, use -h for help")