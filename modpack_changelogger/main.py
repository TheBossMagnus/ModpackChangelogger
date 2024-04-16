import argparse
import logging
import os
import sys

from .compare_packs import compare_packs
from .config_handler import create_config, load_config
from .constants import VERSION
from .extract_pack_data import cf_get_pack_data, mr_get_pack_data
from .get_json import get_json
from .out import markdown_out
from .overrides_detection import add_overrides


def setup_logging(debug):
    # High level logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    # Debug logging to txt file
    if debug:
        # Clear the log file
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("")

        file_handler = logging.FileHandler("log.txt", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M"))
        logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    logger = logging.getLogger(__name__)
    logger.debug("Version: %s", VERSION)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="First pack to compare")
    parser.add_argument("-n", "--new", help="The pack to compare against")
    parser.add_argument("-c", "--config", default=None, nargs="?", const="new", help="Use a config file; 'new' creates a new one")
    parser.add_argument("-f", "--file", default="Changelog.md", help="Specify the output file for the changelog, 'console' prints to console")
    parser.add_argument("-v", "--version", action="store_true", help="Print the version number")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def modpack_changelogger(old_path, new_path, config_path, changelog_file, debug=False):
    # Reset the modpack format
    # This is done so that the program can be called multiple times as an import in the same script
    os.environ["MODPACKS_FORMAT"] = ""
    # Setup logging
    setup_logging(debug)
    logger = logging.getLogger(__name__)

    if debug:
        logger.warning("Debug logging enabled")

    # Handle config creation
    if config_path is not None and config_path.lower() == "new":
        create_config()
        config_path = None
        if not old_path and not new_path:  # If the user only wants to create a new config file
            return

    # Check for required arguments
    if not old_path and not new_path:
        logger.error("ERROR: No packs specified")
        sys.exit(1)
    elif not old_path:
        logger.error("ERROR: No old pack specified")
        sys.exit(1)
    elif not new_path:
        logger.error("ERROR: No new pack specified")
        sys.exit(1)

    # Load config
    config = load_config(config_path)

    # Parse the json files
    old_json, old_config_hash, old_overrides = get_json(old_path)
    new_json, new_config_hash, new_overrides = get_json(new_path)

    # Get pack data based on the modpack format
    if os.getenv("MODPACKS_FORMAT") == "modrinth":
        old_ids, new_ids, old_info, new_info = mr_get_pack_data(old_json, new_json)
    else:
        old_ids, new_ids, old_info, new_info = cf_get_pack_data(old_json, new_json)
    if config["check"]["identified_overrides_mods"] or config["check"]["unidentified_overrides_mods"]:
        old_identified_overrides, new_identified_overrides, old_unidentified_overrides, new_unidentified_overrides = add_overrides(old_overrides, new_overrides, config)
        old_ids = old_ids.union(old_identified_overrides)
        new_ids = new_ids.union(new_identified_overrides)

    # Compare the packs
    added, removed, updated = compare_packs(old_ids, new_ids, old_info, new_info, old_config_hash, new_config_hash, config)
    if config["check"]["unidentified_overrides_mods"]:
        added = added + list(new_unidentified_overrides)
        removed = removed + list(old_unidentified_overrides)

    logger.debug("Added mods: %s\nRemoved mods:%s\nUpdated mods:%s", added, removed, updated)

    # Output the changelog
    markdown_out(added, removed, updated, old_info, new_info, config, changelog_file)


if __name__ == "__main__":
    args = parse_arguments()
    if args.version:
        print(f"ModpackChangelogger {VERSION}")
    modpack_changelogger(args.old, args.new, args.config, args.file, args.debug)