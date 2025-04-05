# This section of the file contains some hardcoded values, do not edit it directly if you don't know what you are doing.

# Import version number from version.py
from .version import __version__ as VERSION

DEFAULT_CONFIG = {
    "check": {"added_mods": True, "removed_mods": True, "updated_mods": True, "loader": True, "mc_version": False, "config": False, "identified_overrides_mods": True, "unidentified_overrides_mods": False},
    "format": {"style": "bullet", "header": {"show_header": True, "size": 2, "title": "auto", "show_old_version_number": False, "show_new_version_number": True}},
}

MR_HEADERS = {"User-Agent": f"TheBossMagnus/ModpackChangelogger/{VERSION} (thebossmagnus@proton.me)"}
MR_API_URL = "https://api.modrinth.com/v2"

# DO NOT USE THIS KEY FOR YOUR OWN PROJECT/FORKS
CF_KEY = "$2a$10$GiT8VjJE8VJpcK68Wlz6aeJ5CPAZcRuTBcGuys8XtX5hGC87sIgku"
# You can get your own key at https://docs.curseforge.com

CF_HEADERS = {"x-api-key": CF_KEY, "Content-Type": "application/json", "Accept": "application/json"}
CF_API_URL = "https://api.curseforge.com/"

# This section of the file contains some utility functions and exception.


def create_config():
    import json

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)


def handle_request_errors(e, url):
    import asyncio

    import aiohttp

    if isinstance(e, aiohttp.ClientConnectionError):
        print("Failed to connect to %s: %s", url, e)
    elif isinstance(e, asyncio.TimeoutError):
        print("The request %s timed out", url)
    elif isinstance(e, aiohttp.ClientResponseError):
        print("Server responded with an error for %s: %s", url, e)
    else:
        print("An unexpected error occurred: %s", e)


class UnsupportedModpackFormatError(Exception):
    """Exception raised for unsupported modpack formats."""

    def __init__(self, path, format):
        self.path = path
        self.format = format
        super().__init__(f"The modpack '{path}' is not in a supported format ({format})")


class DifferentModpackFormatError(Exception):
    """Exception raised for different modpack formats."""

    def __init__(self, old_format, new_format):
        self.old_format = old_format
        self.new_format = new_format
        super().__init__(f"Both modpacks must be in the same format (old: {old_format}, new: {new_format})")


class NoModpackFormatError(Exception):
    """Exception raised when the modpack is wrongly formatted."""

    def __init__(self, path, error):
        self.path = path
        self.error = error
        super().__init__(f"The modpack '{path}' is not packed correctly ({error})")
