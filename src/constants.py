# This file contains some hardcoded values, do not edit it directly if you don't know what you are doing.

# Version number
VERSION = "0.2.0"
# Default config
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
# Networking
HEADERS = {'User-Agent':f"TheBossMagnus/ModpackChangelogger/{VERSION} (thebossmagnus@proton.me)"}
MODRINTH_API_URL = "https://api.modrinth.com/v2"
