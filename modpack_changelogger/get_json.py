import hashlib
import json
import logging
import os
import sys
import tempfile
from zipfile import ZipFile


def get_json(MODPACKS_FORMAT, path):
    if not os.path.exists(path):
        print("ERROR: The file %s does not exist", path)
        sys.exit(1)

    if path.endswith(".mrpack"):
        if MODPACKS_FORMAT == "curseforge":
            print("ERROR: Using Modrinth and a Curseforge modpack together is not supported")
            sys.exit(1)
        MODPACKS_FORMAT = "modrinth"
        logging.debug("Detected Modrinth modpack")
    elif path.endswith(".zip"):
        if MODPACKS_FORMAT == "modrinth":
            print("ERROR: Using Modrinth and a Curseforge modpack together is not supported")
            sys.exit(1)
        MODPACKS_FORMAT = "curseforge"
        logging.debug("Detected CurseForge modpack")
    else:
        print("ERROR: Given modpack is not in a supported format")
        sys.exit(1)

    # Create a temporary directory to extract the modpack into
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Unpack the modpack file into the temp directory
            with ZipFile(path, "r") as zip_obj:
                zip_obj.extractall(path=temp_dir)
                logging.debug("Extracted %s to %s", path, temp_dir)

            # Get config folder hash
            config_hash = hash_directory(os.path.join(temp_dir, "overrides", "config"))
            overrides_name = get_overrides(os.path.join(temp_dir, "overrides", "mods"))

            # Parse the json file
            json_path = os.path.join(temp_dir, "modrinth.index.json" if MODPACKS_FORMAT == "modrinth" else "manifest.json")
            with open(json_path, "r", encoding="utf-8") as json_file:
                logging.debug("Parsed %s", json_path)
                return MODPACKS_FORMAT, json.load(json_file), config_hash, overrides_name
        except FileNotFoundError:
            print("ERROR: The file %s does not exist", json_path)
            sys.exit(1)
        except ValueError:
            print("ERROR: The file %s is not formatted correctly", json_path)
            sys.exit(1)


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
        content = f.read()
        file_hash = hashlib.sha1(content).hexdigest()
    return file_hash


def get_overrides(directory):
    hash_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            hash_dict[file] = calculate_hash(filepath)
    return hash_dict
