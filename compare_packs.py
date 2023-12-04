import re
import asyncio
import logging
from get_mod_name import get_mod_name

def get_mc_version(json):    # Get the minecraft version from the json
    return json['dependencies']['minecraft']

def get_loader(json):    # Get the loader name from the json
    for key in json['dependencies'].keys():
        if key != 'minecraft':
            return key
    return "Unknown"

def get_loader_version(json, loader):    # Get the mod loader version from the json
    return json['dependencies'][loader]

def get_mod_urls(json):    # Get the mod URLs from the json
    return [download for url in json['files'] for download in url['downloads']]

def extract_mod_ids(url_list):    # Extract the mod IDs from the URLs
    pattern = re.compile(r"(?<=data\/)[a-zA-Z0-9]{8}")
    return [pattern.search(str(url)).group(0) for url in url_list]

async def compare_packs(old_json, new_json, config): 

    # Get the some data from both packs
    old_loader = get_loader(old_json)
    new_loader = get_loader(new_json)
    old_loader_version = get_loader_version(old_json, old_loader)
    new_loader_version = get_loader_version(new_json, new_loader)
    old_mc_version = get_mc_version(old_json)
    new_mc_version = get_mc_version(new_json)
    new_urls= set(get_mod_urls(new_json))
    old_urls = set(get_mod_urls(old_json))


    # Remove any URLs that are in both packs (untouched mods)
    new_urls, old_urls = new_urls.difference(old_urls), old_urls.difference(new_urls)

    # Extract the mod IDs from the remaining URLs and convert to sets
    added_ids = set(extract_mod_ids(list(new_urls)))
    removed_ids = set(extract_mod_ids(list(old_urls)))

    updated_ids = added_ids & removed_ids #If they're in both pack, it got updated
    added_ids -= updated_ids # Remove the updated, so only added remain
    removed_ids -= updated_ids # Remove the updated, so only removed remain
    
    # Get the mods names from the Modrinth API via get_mod_name function, ignozre None responses
    if config['check']['added_mods']:
        added_mods = await asyncio.gather(*(get_mod_name(mod_id) for mod_id in added_ids))

    if config['check']['removed_mods']:
        removed_mods = await asyncio.gather(*(get_mod_name(mod_id) for mod_id in removed_ids))

    if config['check']['updated_mods']:
        updated_mods = await asyncio.gather(*(get_mod_name(mod_id) for mod_id in updated_ids))

    # Add loader and mc version changes if enabled in config
    if config['check']['loader']:
        if old_loader != new_loader:    # Loader change
            added_mods.append(f"{new_loader} (mod loader)")
            removed_mods.append(f"{old_loader} (mod loader)")
            logging.debug("Loader change detected: %s, new loader: %s", old_loader, new_loader)
        if old_loader_version != new_loader_version:    # Loader update
            updated_mods.append(f"{new_loader} (mod loader)")
            logging.debug("Loader update detected: %s, new version: %s", old_loader, new_loader_version)
    if old_mc_version != new_mc_version and config['check']['mc_version']:
        updated_mods.append(f"Minecraft version {new_mc_version}")
        logging.debug("Minecraft version change detected: %s, new version: %s", old_mc_version, new_mc_version)

    logging.debug("Added mods: %a\nRemoved mods: %a\nUpdated mods: %a", added_mods, removed_mods, updated_mods)
    
    return sorted(added_mods), sorted(removed_mods), sorted(updated_mods)