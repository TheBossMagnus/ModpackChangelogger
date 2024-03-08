import json
import logging
import os
import sys
from constants import DEFAULT_CONFIG

def create_config():
    try:
        with open("config.json", 'w', encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        logging.info('Created a new config.json')
    except PermissionError:
        logging.error("ERROR: Unable to create the config.json in %s. Try running as administrator", os.getcwd())
        sys.exit(1)

def validate_config(config, default_config):
    """Check if all the fields are present and are of the correct type"""

    if not isinstance(config, dict):
        raise ValueError("Config must be a dictionary")
    for key, default_value in default_config.items():
        if key not in config:
            config[key] = default_value
        elif isinstance(default_value, dict): # Recursively validate nested keys
            config[key] = validate_config(config.get(key, {}), default_value)
        elif not isinstance(config[key], type(default_value)):
            raise ValueError(f"Config field \"{key}\" must be of type {type(default_value).__name__}")
    return config


def load_config(config_file):
    if not config_file:
        logging.debug('CONFIG: Default')
        return DEFAULT_CONFIG

    if not os.path.isfile(config_file):
        logging.error("ERROR: The chosen config file (%s) does not exist", config_file)
        sys.exit(1)

    try:
        logging.debug('CONFIG PATH: %s', config_file)
        with open(config_file, 'r', encoding="utf-8") as f:
            config = json.load(f)
            config = validate_config(config, DEFAULT_CONFIG)
        logging.debug('CONFIG: %s', config)
    except json.JSONDecodeError:
        logging.error("ERROR: %s is not a valid JSON file", config_file)
        sys.exit(1)
    except ValueError as e:
        logging.error("ERROR: %s", e)
        sys.exit(1)

    return config