import re
import sys


def mr_get_pack_data(old_json, new_json):
    PATTERN = re.compile(r"(?<=data\/)[a-zA-Z0-9]{8}")

    def get_dependency_info(json):
        loader = next((key for key in json['dependencies'].keys() if key != 'minecraft'), "Unknown")
        return {
            'mc_version': json['dependencies']['minecraft'],
            'loader': loader,
            'loader_version': json['dependencies'][loader]
        }

    def get_mod_urls(json):
        return [download for url in json['files'] for download in url['downloads']]

    def extract_mod_ids(url_list):
        return [PATTERN.search(str(url)).group(0) for url in url_list]

    old_info, new_info = get_dependency_info(old_json), get_dependency_info(new_json)
    new_urls, old_urls = set(get_mod_urls(new_json)), set(get_mod_urls(old_json))
    # remove urls that are in both packs (not added nor removed nor updated)
    new_urls -= old_urls
    old_urls -= new_urls

    old_ids, new_ids = set(extract_mod_ids(new_urls)), set(extract_mod_ids(old_urls))
    return old_ids, new_ids, old_info, new_info

def cf_get_pack_data(old_json, new_json):
    print("Curseforge support Not yet fully implemented")

    def get_dependency_info(json):
        loader_string = json['minecraft']['modLoaders'][0]['id']
        return {
            'mc_version': json['minecraft']['version'],
            'loader': loader_string.split('-')[0],
            'loader_version': loader_string.split('-')[1]
        }
    

    def analyze_json_files(old_json, new_json):

        old_file_ids = {item['fileID']: item['projectID'] for item in old_json['files']}
        new_file_ids = {item['fileID']: item['projectID'] for item in new_json['files']}

        unique_old_project_ids = set()
        unique_new_project_ids = set()

        for file_id, project_id in old_file_ids.items():
            if file_id not in new_file_ids:
                unique_old_project_ids.add(project_id)

        for file_id, project_id in new_file_ids.items():
            if file_id not in old_file_ids:
                unique_new_project_ids.add(project_id)

        return unique_old_project_ids, unique_new_project_ids
    
    old_info, new_info = get_dependency_info(old_json), get_dependency_info(new_json)
    old_ids, new_ids = analyze_json_files(old_json, new_json)
    print(old_ids, new_ids)
    sys.exit(0)
    return old_ids, new_ids, old_info, new_info
