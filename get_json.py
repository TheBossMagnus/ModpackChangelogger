import os
import json
from zipfile import ZipFile

def get_json(path):
    # Create a temporary directory
    temp_dir = os.path.join(os.environ.get('TEMP'), 'mrpack_Changelogger')
    os.makedirs(temp_dir, exist_ok=True)

    # unpack the .mrpack file into the temp directory
    if path.endswith('.mrpack'):
        with ZipFile(path, 'r') as zObject:
            zObject.extractall(path=temp_dir)
    else:
        raise ValueError('Error: Input file is not a .mrpack')

    # parse the json file
    try:
        with open(os.path.join(temp_dir, 'modrinth.index.json'), 'r', encoding="utf-8") as f:
            return json.load(f)
    except ValueError:
        raise ValueError('Error: modrinth.index.json is not formatted correctly')