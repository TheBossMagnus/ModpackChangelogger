import json
import os
import sys

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

def create_config():
    try:
        with open('config.json', 'w', encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
    except PermissionError:
        print("ERROR: Unable to create the config.json in the current path. Try running as administrator")
        sys.exit(1)

def load_config():
    if not os.path.exists('config.json'):
        return DEFAULT_CONFIG
    try:
        with open('config.json', 'r', encoding="utf-8") as f:
            return json.load(f)
    except ValueError:
        print('WARNING: config.json is not formatted correctly, using defaults value as a fallback')
        return DEFAULT_CONFIG