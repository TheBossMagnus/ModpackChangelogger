import hashlib
import json
import os
import tempfile
from zipfile import ZipFile

from .utils import DifferentModpackFormatError, NoModpackFormatError, UnsupportedModpackFormatError


def get_json(MODPACKS_FORMAT, path):

    if path.endswith(".mrpack"):
        if MODPACKS_FORMAT == "curseforge":
            raise DifferentModpackFormatError("curseforge", "modrinth")
        MODPACKS_FORMAT = "modrinth"

    elif path.endswith(".zip"):
        if MODPACKS_FORMAT == "modrinth":
            raise DifferentModpackFormatError("modrinth", "curseforge")
        MODPACKS_FORMAT = "curseforge"

    else:
        raise UnsupportedModpackFormatError(path, MODPACKS_FORMAT)

    # Create a temporary directory to extract the modpack into
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Unpack the modpack file into the temp directory
            with ZipFile(path, "r") as zip_obj:
                zip_obj.extractall(path=temp_dir)

            # Get config folder hash
            config_hash = hash_directory(os.path.join(temp_dir, "overrides", "config"))
            overrides_name = get_overrides(os.path.join(temp_dir, "overrides", "mods"))

            # Parse the json file
            json_path = os.path.join(temp_dir, "modrinth.index.json" if MODPACKS_FORMAT == "modrinth" else "manifest.json")
            with open(json_path, "r", encoding="utf-8") as json_file:

                return MODPACKS_FORMAT, json.load(json_file), config_hash, overrides_name
        except FileNotFoundError:
            raise NoModpackFormatError(path, "missing manifest.json or modrinth.index.json")
        except ValueError:
            raise NoModpackFormatError(path, "invalid manifest.json or modrinth.index.json")


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
