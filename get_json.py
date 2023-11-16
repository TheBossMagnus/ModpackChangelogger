import os
import json
import sys
import shutil
from zipfile import ZipFile

def get_json(path):
    # Ensure the file is a .mrpack file
    if not path.endswith('.mrpack'):
        print('ERROR: Input file is not a .mrpack')
        sys.exit(1)

    # Create a temporary directory
    temp_dir = os.path.join(os.environ.get('TEMP'), 'mrpack_Changelogger')
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Unpack the .mrpack file into the temp directory
        with ZipFile(path, 'r') as zip_obj:
            zip_obj.extractall(path=temp_dir)

        # Parse the json file
        json_path = os.path.join(temp_dir, 'modrinth.index.json')
        with open(json_path, 'r', encoding="utf-8") as json_file:
            return json.load(json_file)
    except ValueError:
        print(f'ERROR: The file {json_path} is not formatted correctly')
        sys.exit(1)
    finally:
        # Delete the extracted files
        shutil.rmtree(temp_dir)