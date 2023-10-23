import aiohttp

async def get_mod_name(mod_id):
    base_url = "https://api.modrinth.com/v2/project"
    url = base_url + "/" + mod_id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                response_json = await response.json()
                return response_json["title"]
    except aiohttp.ClientResponseError as err:
        print(f"Error: Could not get project info for id {mod_id} from Modrinth API. Response code: {err.status}")
        print("Retry later, if the error persists open an issue on the GitHub repo.")
    except aiohttp.ClientConnectionError as err:
        print(f"Unable to connect do modrinth api,({err}). Check your internet connection and if Modrinth is online.")
    except aiohttp.ClientError as err:
        print(f"Error: {err}")