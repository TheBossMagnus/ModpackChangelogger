import hashlib
import json
import logging
import os
import shutil
import sys
from zipfile import ZipFile

import constants


def get_json(path):
    if not os.path.exists(path):
        logging.error("ERROR: The file %s does not exist", path)
        sys.exit(1)

    if path.endswith(".mrpack"):
        if constants.Modpacks_Format == "curseforge":
            logging.error("ERROR: Using Modrinth and a Curseforge modpack together is not supported")
            sys.exit(1)
        constants.Modpacks_Format = "modrinth"
        logging.debug("Detected Modrinth modpack")
    elif path.endswith(".zip"):
        if constants.Modpacks_Format == "modrinth":
            logging.error("ERROR: Using Modrinth and a Curseforge modpack together is not supported")
            sys.exit(1)
        constants.Modpacks_Format = "curseforge"
        logging.debug("Detected CurseForge modpack")
    else:
        logging.error("ERROR: Given modpack is not in a supported format")
        sys.exit(1)

    # Create a temporary directory
    temp_dir = os.path.join(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp", "ModpackChangelogger")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Unpack the modpack file into the temp directory
        with ZipFile(path, "r") as zip_obj:
            zip_obj.extractall(path=temp_dir)
            logging.debug("Extracted %s to %s", path, temp_dir)

        # Get config folder hash
        config_hash = hash_directory(os.path.join(temp_dir, "overrides", "config"))
        overrides_name = get_overrides(os.path.join(temp_dir, "overrides", "mods"))

        # Parse the json file
        json_path = os.path.join(temp_dir, "modrinth.index.json" if constants.Modpacks_Format == "modrinth" else "manifest.json")
        with open(json_path, "r", encoding="utf-8") as json_file:
            logging.debug("Parsed %s", json_path)
            return json.load(json_file), config_hash, overrides_name
    except FileNotFoundError:
        logging.error("ERROR: The file %s does not exist", json_path)
        sys.exit(1)
    except ValueError:
        logging.error("ERROR: The file %s is not formatted correctly", json_path)
        sys.exit(1)
    finally:
        # Delete the extracted files
        shutil.rmtree(temp_dir)
        logging.debug("Deleted the temp files in %s", temp_dir)


def hash_directory(directory):
    if not os.path.exists(directory):
        return None
    hash_md5 = hashlib.md5()
    for dirpath, _, filenames in os.walk(directory):
        for filename in sorted(filenames):
            with open(os.path.join(dirpath, filename), "rb") as f:
                hash_md5.update(f.read())
    return hash_md5.hexdigest()


def calculate_hash(filename):
    with open(filename, "rb") as f:
        bytes = f.read()  # Read entire file
        hash = hashlib.sha256(bytes).hexdigest()
    return hash


def get_overrides(directory):
    hash_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            hash_dict[file] = calculate_hash(filepath)
    return hash_dict
