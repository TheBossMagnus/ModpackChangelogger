import asyncio
import logging
import re
from get_mod_names import get_mod_names

PATTERN = re.compile(r"(?<=data\/)[a-zA-Z0-9]{8}")

def get_dependency_info(json):
    """
    Extracts dependency information from the provided JSON data.
    Args:
        json (dict): The JSON data of the modpack.
    Returns:
        dict: A dictionary containing the Minecraft version, loader, and loader version.
    """
    loader = next((key for key in json['dependencies'].keys() if key != 'minecraft'), "Unknown")
    return {
        'mc_version': json['dependencies']['minecraft'],
        'loader': loader,
        'loader_version': json['dependencies'][loader]
    }

def get_mod_urls(json):
    """
    Extracts the download URLs of the mods from the provided JSON data.
    """
    return [download for url in json['files'] for download in url['downloads']]

def extract_mod_ids(url_list):
    """
    Extracts the ids of the mods from the urls.
    """
    return [PATTERN.search(str(url)).group(0) for url in url_list]

def compare_packs(old_json, new_json, config):
    """
    Compares two modpacks and generate the diff.
    Args:
        old_json (dict): The JSON data of the old modpack.
        new_json (dict): The JSON data of the new modpack.
        config (dict): The settings.
    Returns:
        tuple: Three sets containing added, removed, and updated elements respectively.
    """
    old_info, new_info = get_dependency_info(old_json), get_dependency_info(new_json)

    new_urls, old_urls = set(get_mod_urls(new_json)), set(get_mod_urls(old_json))
    new_urls, old_urls = new_urls.difference(old_urls), old_urls.difference(new_urls)

    added_ids, removed_ids = set(extract_mod_ids(list(new_urls))), set(extract_mod_ids(list(old_urls)))
    updated_ids = added_ids & removed_ids
    added_ids -= updated_ids
    removed_ids -= updated_ids

    # Remove a category if disabled in config
    if not config['check']['added_mods']:
        added_ids = set()
    if not config['check']['removed_mods']:
        removed_ids = set()
    if not config['check']['updated_mods']:
        updated_ids = set()

    added_mods, removed_mods, updated_mods = asyncio.run(get_mod_names(added_ids, removed_ids, updated_ids))

    added_mods = sorted(mod for mod in added_mods if mod is not None)
    removed_mods = sorted(mod for mod in removed_mods if mod is not None)
    updated_mods = sorted(mod for mod in updated_mods if mod is not None)

    if config['check']['loader']:
        if  old_info['loader'] != new_info['loader']:
            added_mods.append(f"{new_info['loader']} (mod loader)")
            removed_mods.append(f"{old_info['loader']} (mod loader)")
            logging.debug("Loader change detected: %s, new loader: %s", old_info['loader'], new_info['loader'])
        elif old_info['loader_version'] != new_info['loader_version']:
            updated_mods.append(f"{new_info['loader']} (mod loader)")
            logging.debug("Loader update detected: %s, new version: %s", old_info['loader'], new_info['loader_version'])

    if config['check']['mc_version'] and old_info['mc_version'] != new_info['mc_version']:
        updated_mods.append(f"Minecraft version {new_info['mc_version']}")
        logging.debug("Minecraft version change detected: %s, new version: %s", old_info['mc_version'], new_info['mc_version'])

    logging.debug("Added mods: %a\nRemoved mods: %a\nUpdated mods: %a", added_mods, removed_mods, updated_mods)

    return added_mods, removed_mods, updated_mods