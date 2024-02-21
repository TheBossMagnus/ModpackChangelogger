import json
import logging
import os
import sys
from constants import DEFAULT_CONFIG

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
        logging.debug('CONFIG: Default')
        return DEFAULT_CONFIG
    if config_file and config_file.lower() == 'new':
        create_config()
        logging.debug('CONFIG: Default')
        return DEFAULT_CONFIG

    if not os.path.isfile(config_file):
        logging.error("ERROR: The chosen config file (%s) does not exist", config_file)
        sys.exit(1)

    try:
        with open(config_file, 'r', encoding="utf-8") as f:
            config = json.load(f)
        logging.debug('Loaded config from %s', config_file)
        return config
    except ValueError:
        logging.error("ERROR: %s is not formatted correctly", config_file)
        sys.exit(1)