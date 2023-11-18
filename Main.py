import asyncio
import logging
import argparse
from compare_packs import compare_packs
from out import markdown_out
from get_json import get_json
from config_handler import load_config, create_config

# Initialize the logger
logger = logging.getLogger(__name__)
import logging

# Set up the root logger
def setup_logging(debug):
    # Set up a file handler with a lower level (e.g., DEBUG)
    file_handler = logging.FileHandler('log.txt')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Set up a console handler with a higher level (e.g., INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    # Add the handlers to the root logger
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, handlers=[file_handler, console_handler])

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

    setup_logging(args.debug)

    if args.debug:
        logger.info("Debug logging enabled")

    if args.create_config:
        create_config()
    if args.old and args.new:
        main(args.old, args.new)

if __name__ == "__main__":
    handle_arguments()