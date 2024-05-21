import logging
import sys
import traceback

from .compare_packs import compare_packs
from .config_handler import create_config, load_config
from .constants import VERSION
from .extract_pack_data import cf_get_pack_data, mr_get_pack_data
from .get_json import get_json
from .out import markdown_out
from .overrides_detection import add_overrides


def setup_logging(debug):
    if debug:
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write("")

        file_handler = logging.FileHandler("log.txt", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M"))

        logging.basicConfig(level=logging.DEBUG, handlers=[file_handler])
        print("Debug logging enabled")

    logger = logging.getLogger(__name__)
    logger.debug("Version: %s", VERSION)

    def log_all_exceptions(type, value, tb):
        logger.error("Uncaught exception: ", exc_info=(type, value, tb))

    sys.excepthook = log_all_exceptions


def generate_changelog(old_path, new_path, config_path, changelog_file, debug=False):
    create_config()

    # Setup logging
    setup_logging(debug)
    logger = logging.getLogger(__name__)

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
    MODPACKS_FORMAT, old_json, old_config_hash, old_overrides = get_json(None, old_path)  # None means that the format is not yet known, so it will be whatever detected by the function
    MODPACKS_FORMAT, new_json, new_config_hash, new_overrides = get_json(MODPACKS_FORMAT, new_path)  # The format is now known, so the function checks it is the same as the old one

    # Get pack data based on the modpack format
    if MODPACKS_FORMAT == "modrinth":
        old_ids, new_ids, old_info, new_info = mr_get_pack_data(old_json, new_json)
    else:
        old_ids, new_ids, old_info, new_info = cf_get_pack_data(old_json, new_json)
    if config["check"]["identified_overrides_mods"] or config["check"]["unidentified_overrides_mods"]:
        old_identified_overrides, new_identified_overrides, old_unidentified_overrides, new_unidentified_overrides = add_overrides(MODPACKS_FORMAT, old_overrides, new_overrides, config)
        old_ids = old_ids.union(old_identified_overrides)
        new_ids = new_ids.union(new_identified_overrides)

    # Compare the packs
    added, removed, updated = compare_packs(MODPACKS_FORMAT, old_ids, new_ids, old_info, new_info, old_config_hash, new_config_hash, config)
    if config["check"]["unidentified_overrides_mods"]:
        added = added + list(new_unidentified_overrides)
        removed = removed + list(old_unidentified_overrides)

    logger.debug("Added mods: %s\nRemoved mods:%s\nUpdated mods:%s", added, removed, updated)

    if changelog_file is None:
        changelog_file = "Changelog.md"

    if changelog_file.lower() == "unformatted":
        logging.debug("Returned as unformatted changelog")
        return added, removed, updated
    if changelog_file.lower() == "formatted":
        logging.debug("Returned as formatted changelog")
        return markdown_out(added, removed, updated, old_info, new_info, config, None)  # if changelog_file is None, it will return the markdown text
    if changelog_file.lower() == "console":
        logging.debug("Printed changelog to console")
        print(markdown_out(added, removed, updated, old_info, new_info, config, None))
    else:
        markdown_out(added, removed, updated, old_info, new_info, config, changelog_file)
