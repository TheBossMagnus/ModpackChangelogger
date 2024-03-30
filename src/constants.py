# This file contains some hardcoded values, do not edit it directly if you don't know what you are doing.

# Mod ecosistem used (modrinth or curseforge)
# It gets auto detected
Modpacks_Format = None
# Version number
VERSION = "0.3.2"
# Default config
DEFAULT_CONFIG = {
    "check": {
        "added_mods": True,
        "removed_mods": True,
        "updated_mods": True,
        "loader": True,
        "mc_version": False,
        "config": False,
        "EXPERIMENTAL_overrides_mods": False
    },
    "format": {
        "style": "bullet",
        "header": {
            "show_header": True,
            "size": 2,
            "title": "auto",
            "show_old_version_number": False,
            "show_new_version_number": True
        }
    },
}
# Networking
MR_HEADERS = {"User-Agent": f"TheBossMagnus/ModpackChangelogger/{VERSION} (thebossmagnus@proton.me)"}
MR_API_URL = "https://api.modrinth.com/v2/projects?ids="

# DO NOT USE THIS KEY FOR YOUR OWN PROJECT/FORKS
CF_KEY = "$2a$10$GiT8VjJE8VJpcK68Wlz6aeJ5CPAZcRuTBcGuys8XtX5hGC87sIgku"
# You can get your own key at https://docs.curseforge.com

CF_HEADERS = {"x-api-key": CF_KEY, "Content-Type": "application/json", "Accept": "application/json"}
CF_API_URL = "https://api.curseforge.com/v1/mods"
