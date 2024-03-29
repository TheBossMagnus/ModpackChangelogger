import asyncio
import json
import logging
import aiohttp
from constants import MR_API_URL, MR_HEADERS, CF_HEADERS, CF_API_URL
import constants

async def get_mod_names(added_ids, removed_ids, updated_ids):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        api_function = {
            "modrinth": request_from_mr_api,
            "curseforge": request_from_cf_api
        }.get(constants.Modpacks_Format)

        added_names, removed_names, updated_names = await asyncio.gather(
            api_function(session, added_ids),
            api_function(session, removed_ids),
            api_function(session, updated_ids)
        )

        return added_names, removed_names, updated_names

async def request_from_mr_api(session, ids):
    if not ids:
        return []
 
    names = []
    URL = f"{MR_API_URL}{json.dumps(list(ids))}"

    try:
        async with session.get(URL, headers=MR_HEADERS) as response:
            response.raise_for_status()
            data = await response.json()
            names = [project.get('title') for project in data]
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError, aiohttp.ClientResponseError) as e:
        handle_request_errors(e, URL)

    return names

async def request_from_cf_api(session, ids):
    if not ids:
        return [] 

    names = []
    URL = f"{CF_API_URL}"

    try:
        async with session.post(URL, headers=CF_HEADERS, json={'modIds': list(ids)}) as response:
            response = await response.json()
            names = [project['name'] for project in response['data']]
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError, aiohttp.ClientResponseError) as e:
        handle_request_errors(e, URL)

    return names

def handle_request_errors(e, URL):
    if isinstance(e, aiohttp.ClientConnectionError):
        logging.warning("Failed to connect to %s: %s", URL, e)
    elif isinstance(e, asyncio.TimeoutError):
        logging.warning("The request %s timed out", URL)
    elif isinstance(e, aiohttp.ClientResponseError):
        logging.warning("Server responded with an error for %s: %s", URL, e)
    else:
        logging.warning("An unexpected error occurred: %s", e)
