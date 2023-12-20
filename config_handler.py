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
}

def create_config():
    try:
        with open("config.json", 'w', encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
            logging.debug('Created config.json')
    except PermissionError:
        logging.error("ERROR: Unable to create the config.json in %s. Try running as administrator", os.getcwd())
        sys.exit(1)

def load_config(config_file):
    if not config_file:
        return DEFAULT_CONFIG
    if not os.path.isfile(config_file):
        logging.error("ERROR: The chose config file (%s) does not exist", config_file)
        sys.exit(1)
    try:
        with open(config_file, 'r', encoding="utf-8") as f:
            logging.debug('Loaded config from %s', config_file)
            return json.load(f)
    except ValueError:
        logging.error("ERROR: %s is not formatted correctly", config_file)
        sys.exit(1)