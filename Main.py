import sys
import argparse
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json
from config_handler import load_config, create_config
   
# create the top-level parser
parser = argparse.ArgumentParser(description="Get the changelog between two .mrpack minecraft's modpacks")

# add arguments for old_path and new_path
parser.add_argument("-o", "--old", help="Old file")
parser.add_argument("-n", "--new", help="New file")

# create the subparsers for commands
subparsers = parser.add_subparsers(dest='command')

# create the parser for the "config" command
config_parser = subparsers.add_parser('config', help='Manage the config.json')
config_parser.add_argument('action', choices=['init'], help='Create a config.json file with default values')

# parse the arguments
args = parser.parse_args()

if args.command == 'config':
    create_config()
    sys.exit(0)
elif args.old and args.new:
    pass
else:
    parser.print_help()
    sys.exit(1)

config = load_config()

# Parse the json files
old_json = get_json(args.old)
new_json = get_json(args.new)

# Compare the packs
added, removed, updated = compare_packs(old_json, new_json, config)

# Print in a md doc
markdown_out(added, removed, updated, config)