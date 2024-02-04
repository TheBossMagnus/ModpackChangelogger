import asyncio
import json
import logging
import aiohttp
from constants import MR_API_URL, MR_HEADERS, CF_HEADERS, CF_API_URL
import constants

async def get_mod_names(added_ids, removed_ids, updated_ids):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        added_names, removed_names, updated_names = await asyncio.gather(
            request_from_api(session, added_ids),
            request_from_api(session, removed_ids),
            request_from_api(session, updated_ids)
        )
        return added_names, removed_names, updated_names

async def request_from_api(session, ids):
    # Convert the set of ids to a json array
    ids_list = json.dumps(list(ids))
    names = []
    if constants.Modpacks_Format == "modrinth":
        URL = f"{MR_API_URL}/projects?ids={ids_list}"

        try:
            async with session.get(URL, headers=CF_HEADERS) as response:
                response.raise_for_status()
                data = await response.json()
                names = [project.get('title') for project in data]
        except aiohttp.ClientConnectionError as e:
            logging.warning("Failed to connect to %s: %s", URL, e)
        except asyncio.TimeoutError:
            logging.warning("The request %s timed out", URL)
        except aiohttp.ClientResponseError as e:
            logging.warning("Server responded with an error for %s: %s", URL, e)
        except aiohttp.ClientPayloadError as e:
            logging.warning("Failed to read response from %s: %s", URL, e)
        except aiohttp.ClientError as e:
            logging.warning("An unexpected error occurred: %s", e)
        
    elif constants.Modpacks_Format == "curseforge":
        URL = f"{CF_API_URL}/v1/mods"
        headers = {
            'x-api-key': '$2a$10$GiT8VjJE8VJpcK68Wlz6aeJ5CPAZcRuTBcGuys8XtX5hGC87sIgku',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {'modIds': [348521, 238222]}

        try:
            async with session.post(URL, headers=headers, json=data, ssl=False) as response:
                response.raise_for_status()
                data = await response.json()
                names = [project.get('name') for project in data]
        except aiohttp.ClientConnectionError as e:
            logging.warning("Failed to connect to %s: %s", URL, e)
        except asyncio.TimeoutError:
            logging.warning("The request %s timed out", URL)
        except aiohttp.ClientResponseError as e:
            logging.warning("Server responded with an error for %s: %s", URL, e)
        except aiohttp.ClientPayloadError as e:
            logging.warning("Failed to read response from %s: %s", URL, e)
        except aiohttp.ClientError as e:
            logging.warning("An unexpected error occurred: %s", e)

    return names