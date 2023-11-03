import aiohttp

async def get_mod_name(mod_id):
    base_url = "https://api.modrinth.com/v2/project"
    headers = {'User-Agent':"TheBossMagnus/Mrpack_changelogger (thebossmagnus@proton.me)"}
    url = base_url + "/" + mod_id

    try:
        #Get mod name
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                response_json = await response.json()
                return response_json["title"]
    #ID not existing or similar
    except aiohttp.ClientResponseError as err:
        print(f"WARNING: Could not get project info for id {mod_id} from Modrinth API. Response code: {err.status}")
        print("Retry later, if the error persists open an issue on the GitHub repo.")
    #Connection error
    except aiohttp.ClientConnectionError as err:
        print(f"WARNING: Unable to connect to modrinth api, ({err}). Check your internet connection and if Modrinth is online.")
    #Generic error
    except aiohttp.ClientError as err:
        print(f"ERROR: {err}")
