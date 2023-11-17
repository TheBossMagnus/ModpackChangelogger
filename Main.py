import asyncio
import logging
import argparse
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json
from config_handler import load_config, create_config

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main(old_path, new_path):
    config = load_config()

    # Parse the json files
    old_json = get_json(old_path)
    new_json = get_json(new_path)

    # Compare the packs
    added, removed, updated = asyncio.run(compare_packs(old_json, new_json, config))

    # Print in a md doc
    markdown_out(added, removed, updated, config)

def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="The pack to compare to")
    parser.add_argument("-n", "--new", help="The pack to compare")
    parser.add_argument("-cc", "--create-config", action="store_true", help="Create a config file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Set up a console handler with a higher level (e.g., INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Set up a file handler with a lower level (e.g., DEBUG)
    file_handler = logging.FileHandler('log.txt')
    file_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    if args.debug:
        logger.info("Debug logging enabled")

    if args.create_config:
        logger.debug("Created config.json")
        create_config()
    if args.old and args.new:
        main(args.old, args.new)

if __name__ == "__main__":
    logger.info("Starting")
    handle_arguments()