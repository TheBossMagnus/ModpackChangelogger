import aiohttp
import asyncio
import logging
from constants import MODRINTH_API_URL, HEADERS

async def get_mod_names(added_ids, removed_ids, updated_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [(request_from_api(session, id_), i) for i, ids in enumerate((added_ids, removed_ids, updated_ids)) for id_ in ids]
        results = await asyncio.gather(*(task for task, _ in tasks))
        added_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 0]
        removed_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 1]
        updated_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 2]
        return added_names, removed_names, updated_names

async def request_from_api(session, id_):
    url = f"{MODRINTH_API_URL}/project/{id_}"
    try:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            data = await response.json()
    except aiohttp.ClientConnectionError as e:
        logging.warning(f"Failed to connect to {url}: {e}")
    except aiohttp.ClientResponseError as e:
        logging.warning(f"Server responded with an error for {url}: {e}")
    except aiohttp.ClientPayloadError as e:
        logging.warning(f"Failed to read response from {url}: {e}")
    except Exception as e:
        logging.warning(f"An unexpected error occurred: {e}")
    else:
        return data.get('title')