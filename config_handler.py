import json
import os
import sys
import logging

# Do not edit this, use config.json
DEFAULT_CONFIG = {
    'check': {
        'added_mods': True,
        'removed_mods': True,
        'updated_mods': True,
        'loader': True,
        'mc_version': False,
    },
    'format': {
        'style': 'bullet'
    },
    'output': {
        'file_name': 'changelog.md',
        'file_path': '',
    },
}
CONFIG_FILE = 'config.json'

def create_config():
    try:
        with open(CONFIG_FILE, 'w', encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
            logging.debug('Created config.json')
    except PermissionError:
        logging.error("ERROR: Unable to create the config.json in the current path. Try running as administrator")
        sys.exit(1)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        logging.debug('no config.json present, using default values')
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
            logging.debug('Loaded config.json')
            return json.load(f)
    except ValueError:
        logging.warning('WARNING: config.json is not formatted correctly, using defaults value as a fallback')
        return DEFAULT_CONFIG