import asyncio
import logging
import argparse
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json
from config_handler import load_config, create_config

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
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[console_handler])


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="The pack to compare to")
    parser.add_argument("-n", "--new", help="The pack to compare")
    parser.add_argument("-c", "--config", nargs='?', const='new', help="Choose or create a config file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def main(old_path, new_path, config_path):
    config = load_config(config_path)
    # Parse the json files
    old_json = get_json(old_path)
    new_json = get_json(new_path)
    # Compare the packs
    added, removed, updated = asyncio.run(compare_packs(old_json, new_json, config))
    # Print in a md doc
    markdown_out(added, removed, updated, config)

if __name__ == "__main__":
    args = parse_arguments()
    logger = logging.getLogger(__name__)
    setup_logging(args.debug)

    if args.debug:
        logger.info("Debug logging enabled")
        logging.debug("Arguments: %a", args)
    if args.config == 'new':
        args.config = None
        create_config()
    if args.old and args.new:
        main(args.old, args.new, args.config)