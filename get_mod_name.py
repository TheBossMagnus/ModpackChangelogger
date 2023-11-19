import logging
from aiohttp import ClientSession, ClientResponseError, ClientConnectionError, ClientError

async def get_mod_name(mod_id):
    base_url = "https://api.modrinth.com/v2/project"
    headers = {'User-Agent':"TheBossMagnus/Mrpack_changelogger (thebossmagnus@proton.me)"}
    url = f"{base_url}/{mod_id}"

    try:
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                response_json = await response.json()
                logging.debug("Successfully retrieved name %s for ID %s", response_json.get('title'), mod_id)
                return response_json.get('title')
    except ClientResponseError as err:
        logging.warning("WARNING: Unable to retrieve project information for ID %s from Modrinth API. Received response code: %s", mod_id, err.status)
        logging.info("If the issue persists, consider reporting it on GitHub repository.")
    except ClientConnectionError:
        logging.warning("WARNING: Connection to the Modrinth API failed. Please ensure your internet connection is stable and that Modrinth is currently accessible.")
    except ClientError as err:
        logging.warning("Warning: Unable to connect to the Modrinth API. The following error occurred: %s", err)