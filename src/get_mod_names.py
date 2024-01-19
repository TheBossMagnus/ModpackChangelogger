import logging
import asyncio
import aiohttp
from constants import MODRINTH_API_URL, HEADERS

async def get_mod_names(added_ids, removed_ids, updated_ids):
    """
    Handle the Asynchronously fetches of the names.
    Args:
        added_ids, updated_ids, removed_ids: Lists of IDs.
    Returns: 
        lists containing the names of added, removed, and updated mods respectively.
        """
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        # Merge the list of ids and run the web request
        tasks = [(request_from_api(session, id_), i) for i, ids in enumerate((added_ids, removed_ids, updated_ids)) for id_ in ids]
        results = await asyncio.gather(*(task for task, _ in tasks))
        # Split the list back
        added_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 0]
        removed_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 1]
        updated_names = [result for result, index in zip(results, (index for _, index in tasks)) if index == 2]
        return added_names, removed_names, updated_names

async def request_from_api(session, id_):
    """
    Asynchronously sends a GET request to the Modrinth API and returns the response.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        id_ (str): The ID of the mod to fetch.

    Returns:
        dict: The mod name form the json.
    """
    URL = f"{MODRINTH_API_URL}/project/{id_}"
    try:
        async with session.get(URL, headers=HEADERS) as response:
            response.raise_for_status()
            data = await response.json()
    except aiohttp.ClientConnectionError as e:
        logging.warning("Failed to connect to %s: %s", URL, e)
    except asyncio.TimeoutError:
        logging.warning("The request %s timed out ", URL)
    except aiohttp.ClientResponseError as e:
        logging.warning("Server responded with an error for %s: %s", URL, e)
    except aiohttp.ClientPayloadError as e:
        logging.warning("Failed to read response from %s: %s", URL, e)
    except aiohttp.ClientError as e:
        logging.warning("An unexpected error occurred: %s", e)
    else:
        return data.get('title')