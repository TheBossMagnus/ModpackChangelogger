import argparse
import logging
from compare_packs import compare_packs
from config_handler import load_config
from constants import VERSION
from get_json import get_json
from out import markdown_out

def setup_logging(debug):
    # High level logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    # Debug logging to txt file
    if debug:
        # Clear the log file
        with open('log.txt', 'w', encoding="utf-8") as f:
            f.write('')
        
        file_handler = logging.FileHandler('log.txt', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M'))
        logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    logger = logging.getLogger(__name__)
    logger.debug("Version: %s", VERSION)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="First pack to compare")
    parser.add_argument("-n", "--new", help="The pack to compare against")
    parser.add_argument("-c", "--config", default=None, nargs='?', const='new', help="Use a config file; 'new' creates a new one")
    parser.add_argument("-f", "--file", default=None, help="Specify the output file for the changelog, 'console' prints to console")
    parser.add_argument("-v", "--version", action="store_true", help="Print the version number")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def main(old_path, new_path, config_path, changelog_file, debug=False):
    setup_logging(debug)
    logger = logging.getLogger(__name__)

    config = load_config(config_path)

    if not old_path or not new_path:
        if not old_path and new_path:
            logger.error("ERROR: No old pack specified")
        if not new_path and old_path:
            logger.error("ERROR: No new pack specified")
        return

    # Parse the json files
    old_json = get_json(old_path)
    new_json = get_json(new_path)

    # Compare the packs
    added, removed, updated = compare_packs(old_json, new_json, config)
    # Print in a md doc
    markdown_out(added, removed, updated, config, changelog_file)

if __name__ == "__main__":
    args = parse_arguments()
    if args.version:
        print(f"ModpackChangelogger {VERSION}")
    main(args.old, args.new, args.config, args.file, args.debug)
