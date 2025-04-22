import re


def mr_get_pack_data(old_json, new_json):
    pattern = re.compile(r"(?<=data\/)[a-zA-Z0-9]{8}")

    def get_dependency_info(json):
        loader = next(
            (key for key in json.get("dependencies", {}) if key != "minecraft"),
            "Unknown",
        )
        return {
            "modpack_name": json.get("name", "Unknown"),
            "modpack_version": json.get("versionId", "Unknown"),
            "mc_version": json.get("dependencies", {}).get("minecraft", "Unknown"),
            "loader": loader,
            "loader_version": json.get("dependencies", {}).get(loader, "Unknown"),
        }

    def get_mod_urls(json):
        return [download for url in json["files"] for download in url["downloads"]]

    def extract_mod_ids(url_list):
        return [pattern.search(str(url)).group(0) for url in url_list]

    old_info, new_info = get_dependency_info(old_json), get_dependency_info(new_json)
    new_urls, old_urls = set(get_mod_urls(new_json)), set(get_mod_urls(old_json))
    # remove urls that are in both packs (not added nor removed nor updated)
    common_urls = new_urls & old_urls
    new_urls -= common_urls
    old_urls -= common_urls

    old_ids, new_ids = set(extract_mod_ids(old_urls)), set(extract_mod_ids(new_urls))
    return old_ids, new_ids, old_info, new_info


def cf_get_pack_data(old_json, new_json):
    def get_dependency_info(json):
        loader_string = (
            json.get("minecraft", {})
            .get("modLoaders", [{}])[0]
            .get("id", "Unknown-Unknown")
        )
        loader, loader_version = (
            loader_string.split("-", 1)
            if "-" in loader_string
            else ("Unknown", "Unknown")
        )
        return {
            "modpack_name": json.get("name", "Unknown"),
            "modpack_version": json.get("version", "Unknown"),
            "mc_version": json.get("minecraft", {}).get("version", "Unknown"),
            "loader": loader,
            "loader_version": loader_version,
        }

    def get_mod_ids(json):
        # Extracts the file and project IDs from the JSON
        return {item["fileID"]: item["projectID"] for item in json["files"]}

    old_file_ids = get_mod_ids(old_json)
    new_file_ids = get_mod_ids(new_json)

    # To reference a file cf has a project id (the mod) and a file id (the version)
    # with this code we can get mod that have been changed between the two packs, so with unquie file ids
    old_ids = {
        old_file_ids[file_id] for file_id in old_file_ids if file_id not in new_file_ids
    }
    new_ids = {
        new_file_ids[file_id] for file_id in new_file_ids if file_id not in old_file_ids
    }

    old_info, new_info = get_dependency_info(old_json), get_dependency_info(new_json)
    return old_ids, new_ids, old_info, new_info
