import logging
import asyncio
import aiohttp
from constants import MODRINTH_API_URL, HEADERS

async def get_mod_names(added_ids, removed_ids, updated_ids):
    async with aiohttp.ClientSession() as session:
        # Merge the list of ids and run the web request
        tasks = [(request_from_api(session, id_), i) for i, ids in enumerate((added_ids, removed_ids, updated_ids)) for id_ in ids]
        results = await asyncio.gather(*(task for task, _ in tasks))
        # Split the list back
        added_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 0]
        removed_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 1]
        updated_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 2]
        return added_names, removed_names, updated_names

async def request_from_api(session, id_):
    URL = f"{MODRINTH_API_URL}/project/{id_}"
    try:
        async with session.get(URL, headers=HEADERS) as response:
            response.raise_for_status()
            data = await response.json()
    except aiohttp.ClientConnectionError as e:
        logging.warning("Failed to connect to %s: %s", URL, e)
    except aiohttp.ClientResponseError as e:
        logging.warning("Server responded with an error for %s: %s", URL, e)
    except aiohttp.ClientPayloadError as e:
        logging.warning("Failed to read response from %s: %s", URL, e)
    except Exception as e:
        logging.warning("An unexpected error occurred: %s", e)
    else:
        return data.get('title')