# This file is a cli wrapper for the modpack_changelogger function in main.py
# It's a kinda hacky way to make the script callable from the command line and add a cli entrypoint to the package
import argparse

from .constants import VERSION
from .main import generate_changelog


def wrapper():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="First pack to compare")
    parser.add_argument("-n", "--new", help="The pack to compare against")
    parser.add_argument("-c", "--config", default=None, nargs="?", const="new", help="Use a config file; 'new' creates a new one")
    parser.add_argument("-f", "--file", default=None, help="Specify the output file for the changelog, 'console' prints to console")
    parser.add_argument("-v", "--version", action="store_true", help="Print the version number")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    if args.version:
        print(f"ModpackChangelogger {VERSION}")
    generate_changelog(args.old, args.new, args.config, args.file, args.debug)
