import asyncio
import json
import logging

import aiohttp

import constants
from constants import CF_API_URL, CF_HEADERS, MR_API_URL, MR_HEADERS


async def get_mod_names(added_ids, removed_ids, updated_ids):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        api_function = {"modrinth": request_from_mr_api, "curseforge": request_from_cf_api}.get(constants.Modpacks_Format)

        added_names, removed_names, updated_names = await asyncio.gather(api_function(session, added_ids), api_function(session, removed_ids), api_function(session, updated_ids))

        return added_names, removed_names, updated_names


async def request_from_mr_api(session, ids):
    if not ids:
        return []

    names = []
    url = f"{MR_API_URL}/projects?ids={json.dumps(list(ids))}"

    try:
        async with session.get(url, headers=MR_HEADERS) as response:
            response.raise_for_status()
            data = await response.json()
            names = [project.get("title") for project in data]
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError, aiohttp.ClientResponseError) as e:
        handle_request_errors(e, url)

    return names


async def request_from_cf_api(session, ids):
    if not ids:
        return []

    names = []
    url = f"{CF_API_URL}v1/mods"

    try:
        async with session.post(url, headers=CF_HEADERS, json={"modIds": list(ids)}) as response:
            response = await response.json()
            names = [project["name"] for project in response["data"]]
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError, aiohttp.ClientResponseError) as e:
        handle_request_errors(e, url)

    return names


def handle_request_errors(e, url):
    if isinstance(e, aiohttp.ClientConnectionError):
        logging.warning("Failed to connect to %s: %s", url, e)
    elif isinstance(e, asyncio.TimeoutError):
        logging.warning("The request %s timed out", url)
    elif isinstance(e, aiohttp.ClientResponseError):
        logging.warning("Server responded with an error for %s: %s", url, e)
    else:
        logging.warning("An unexpected error occurred: %s", e)
