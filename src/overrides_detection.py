import asyncio
import logging

import aiohttp

import constants


def add_overrides(old_overrides, new_overrides):

    identical_entries = set(old_overrides.values()) & set(new_overrides.values())
    old_overrides = {key: value for key, value in old_overrides.items() if value not in identical_entries}
    new_overrides = {key: value for key, value in new_overrides.items() if value not in identical_entries}

    async def get_names_from_hashes(dict1, dict2):
        async with aiohttp.ClientSession() as session:
            for d in [dict1, dict2]:
                for key in list(d.keys()):
                    async with session.get(f"{constants.MR_API_URL}/version_file/{d[key]}", headers=constants.MR_HEADERS) as response:
                        if response.status == 200:
                            data = await response.json()
                            project_name = data["project_id"]
                            d[key] = project_name
                            logging.debug(f'Found overrides from project id "{project_name}"')
                        else:
                            d[key] = None

    if constants.Modpacks_Format == "modrinth":
        asyncio.run(get_names_from_hashes(old_overrides, new_overrides))

    return {key for key in old_overrides.values() if key is not None}, {key for key in new_overrides.values() if key is not None}
