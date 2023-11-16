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

def print_help():
    print("Usage:")
    print("  -o, --old                   The pack to compare to")
    print("  -n, --new                   The pack to compare")
    print("  -cc, --create-config        Create a config file")
    print("  -h, --help                  show this help message and exit")

def handle_arguments():
    if sys.argv[1] in {"-cc", "--create-config"}:
        create_config()
        sys.exit(0)
    elif sys.argv[1] in {"-o", "--old"} and sys.argv[3] in {"-n", "--new"}:
        main(sys.argv[2], sys.argv[4])
    elif sys.argv[1] in {"-h", "--help", "-?"}:
        print_help()
        sys.exit(0)
    else:
        print("ERROR: Invalid arguments, use -h for help")
        sys.exit(1)

if __name__ == "__main__":
    handle_arguments()