def GetModName(ModId):
    import requests
    BaseUrl = "https://api.modrinth.com/v2/project"
    Url = BaseUrl + "/" + ModId

    try:
        response = requests.get(Url)
        response.raise_for_status()
        responseJson = response.json()
        return responseJson["title"]
    except requests.exceptions.HTTPError as err:
        print(f"Error: Could not get project info for id {ModId} from Modrinth API. Response code: {err.response.status_code}")
        print("Retry later, if the error persists open an issue on the GitHub repo.")
    except requests.exceptions.ConnectionError as err:
        print(f"Unable to connect do modrinth api,({err}). Check your internet connection and if Modrinth is online.")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")