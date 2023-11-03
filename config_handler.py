import json
import os

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
    } 
}

def create_config():
    with open('config.json', 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)

def load_config():
    if not os.path.exists('config.json'):
        return DEFAULT_CONFIG
    else:
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except ValueError:
            print('Warning: config.json is not formatted correctly, using defaults value as a fallback')
            return DEFAULT_CONFIG