import re
import asyncio
import logging
from get_mod_names import get_mod_names
PATTERN = re.compile(r"(?<=data\/)[a-zA-Z0-9]{8}")

def get_mc_version(json):
    return json['dependencies']['minecraft']

def get_loader(json):
    return next((key for key in json['dependencies'].keys() if key != 'minecraft'), "Unknown")

def get_loader_version(json, loader):
    return json['dependencies'][loader]

def get_mod_urls(json):
    return [download for url in json['files'] for download in url['downloads']]

def extract_mod_ids(url_list):
    return [PATTERN.search(str(url)).group(0) for url in url_list]

async def compare_packs(old_json, new_json, config):
    old_loader, new_loader = get_loader(old_json), get_loader(new_json)
    old_loader_version, new_loader_version = get_loader_version(old_json, old_loader), get_loader_version(new_json, new_loader)
    old_mc_version, new_mc_version = get_mc_version(old_json), get_mc_version(new_json)

    new_urls, old_urls = set(get_mod_urls(new_json)), set(get_mod_urls(old_json))
    new_urls, old_urls = new_urls.difference(old_urls), old_urls.difference(new_urls)

    added_ids, removed_ids = set(extract_mod_ids(list(new_urls))), set(extract_mod_ids(list(old_urls)))
    updated_ids = added_ids & removed_ids
    added_ids -= updated_ids
    removed_ids -= updated_ids

    added_mods, removed_mods, updated_mods = await get_mod_names(added_ids, removed_ids, updated_ids)

    if config['check']['loader']:
        if old_loader != new_loader:
            added_mods.append(f"{new_loader} (mod loader)")
            removed_mods.append(f"{old_loader} (mod loader)")
            logging.debug("Loader change detected: %s, new loader: %s", old_loader, new_loader)
        if old_loader_version != new_loader_version:
            updated_mods.append(f"{new_loader} (mod loader)")
            logging.debug("Loader update detected: %s, new version: %s", old_loader, new_loader_version)

    if old_mc_version != new_mc_version and config['check']['mc_version']:
        updated_mods.append(f"Minecraft version {new_mc_version}")
        logging.debug("Minecraft version change detected: %s, new version: %s", old_mc_version, new_mc_version)

    logging.debug("Added mods: %a\nRemoved mods: %a\nUpdated mods: %a", added_mods, removed_mods, updated_mods)

    return sorted(added_mods), sorted(removed_mods), sorted(updated_mods)