import json
import os
import sys

from .constants import DEFAULT_CONFIG


def create_config():
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)


def validate_config(config, default_config):
    """Check if all the fields are present and are of the correct type"""

    for key, default_value in default_config.items():
        if key not in config:
            config[key] = default_value
        elif isinstance(default_value, dict):  # Recursively validate nested keys
            config[key] = validate_config(config.get(key, {}), default_value)
        elif not isinstance(config[key], type(default_value)):
            raise ValueError(f'Config field "{key}" must be of type {type(default_value).__name__}')
    return config


def load_config(config_file):
    if not config_file:
        return DEFAULT_CONFIG

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
        config = validate_config(config, DEFAULT_CONFIG)

    return config
