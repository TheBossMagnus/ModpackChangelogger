import asyncio
import logging
from get_mod_names import get_mod_names


def compare_packs(old_ids, new_ids, old_info, new_info, config):

    updated_ids = old_ids & new_ids
    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids

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