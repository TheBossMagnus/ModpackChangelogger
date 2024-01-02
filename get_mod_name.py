import logging
import aiohttp
from constants import BASE_URL, HEADERS

async def get_mod_name(session, mod_id):
    url = f"{BASE_URL}/{mod_id}"

    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            response.raise_for_status()
            response_json = await response.json()
            mod_name = response_json.get('title')
            logging.debug("Successfully retrieved name %s for ID %s", mod_name, mod_id)
            return mod_name
    except aiohttp.ClientResponseError as err:
        logging.warning("WARNING: Unable to retrieve project information for ID %s from Modrinth API. Received response code: %s. If the issue persists, consider reporting it on GitHub repository.", mod_id, err.status)
    except aiohttp.ClientConnectionError:
        logging.warning("WARNING: Connection to the Modrinth API failed. Please ensure your internet connection is stable and that Modrinth is currently accessible.")
    except aiohttp.ClientError as err:
        logging.warning("Warning: Unable to connect to the Modrinth API. The following error occurred: %s", err)