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
                return response_json.get("title")
    except ClientResponseError as err:
        print(f"WARNING: Unable to retrieve project information for ID {mod_id} from Modrinth API. Received response code: {err.status}")
        print("If the issue persists, consider reporting it on GitHub repository.")
    except ClientConnectionError:
        print(f"WARNING: Connection to the Modrinth API failed. Please ensure your internet connection is stable and that Modrinth is currently accessible.")
    except ClientError as err:
        print(f"Warning: Unable to connect to the Modrinth API. The following error occurred: {err}")