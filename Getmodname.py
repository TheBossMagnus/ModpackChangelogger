async def GetModName(ModId):
    import requests
    import asyncio
    import aiohttp

    BaseUrl = "https://api.modrinth.com/v2/project"
    Url = BaseUrl + "/" + ModId

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(Url) as response:
                response.raise_for_status()
                responseJson = await response.json()
                return responseJson["title"]
    except aiohttp.ClientResponseError as err:
        print(f"Error: Could not get project info for id {ModId} from Modrinth API. Response code: {err.status}")
        print("Retry later, if the error persists open an issue on the GitHub repo.")
    except aiohttp.ClientConnectionError as err:
        print(f"Unable to connect do modrinth api,({err}). Check your internet connection and if Modrinth is online.")
    except aiohttp.ClientError as err:
        print(f"Error: {err}")