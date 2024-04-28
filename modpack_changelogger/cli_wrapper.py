# This file is a cli wrapper for the modpack_changelogger function in main.py
# It's a kinda hacky way to make the script callable from the command line and add a cli entrypoint to the package
import argparse

from .constants import VERSION
from .main import generate_changelog


def wrapper():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="First pack to compare")
    parser.add_argument("-n", "--new", help="The pack to compare against")
    parser.add_argument("-c", "--config", help="Use a config file")
    parser.add_argument("-f", "--file", help="Specify the output file for the changelog")
    parser.add_argument("-v", "--version", action="store_true", help="Print the version number")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    if args.version:
        print(f"ModpackChangelogger {VERSION}")
        if not (args.old or args.new or args.config or args.file):  # If the user only wants the version number
            return

    generate_changelog(args.old, args.new, args.config, args.file, args.debug)
