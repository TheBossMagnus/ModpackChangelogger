# This file is a cli wrapper for the modpack_changelogger function in main.py
# It's a kinda hacky way to make the script callable from the command line and add a cli entrypoint to the package
import argparse
import json
import sys

from .main import generate_changelog
from .utils import VERSION, DifferentModpackFormatError, NoModpackFormatError, UnsupportedModpackFormatError, create_config


def wrapper():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="First pack to compare")
    parser.add_argument("-n", "--new", help="The pack to compare against")
    parser.add_argument("-c", "--config", help="Use a config file")
    parser.add_argument("-f", "--file", help="Specify the output file for the changelog")
    parser.add_argument("-v", "--version", action="store_true", help="Print the version number")
    args = parser.parse_args()

    if args.version:
        print(f"Modpack-Changelogger {VERSION}")
        if not (args.old or args.new or args.config or args.file):  # If the user only wants the version number
            return

    try:
        if args.config == "new":
            create_config()
            args.config = None
            print("Config file created")
            if not (args.old or args.new or args.file):
                return
        generate_changelog(args.old, args.new, args.config, args.file)
    except json.JSONDecodeError as e:
        print(f"ERROR: The json file {e.doc} is not formatted correctly")
        sys.exit(1)
    except PermissionError as e:
        print(f"ERROR: Unable to create or access the file {e.filename}")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR: The file {e.filename} does not exist")
    except UnsupportedModpackFormatError as e:
        print(f"ERROR:{e}")
        sys.exit(1)
    except DifferentModpackFormatError as e:
        print(f"ERROR:{e}")
        sys.exit(1)
    except NoModpackFormatError as e:
        print(f"ERROR:{e}")
        sys.exit(1)
    except Exception as e:
        print(f"UNHANDLED ERROR: {e}")
        print("Please report this issue on the GitHub repository")
        sys.exit(1)
