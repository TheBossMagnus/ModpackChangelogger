import os
import json
import sys
from zipfile import ZipFile

def get_json(path):
    # Create a temporary directory
    temp_dir = os.path.join(os.environ.get('TEMP'), 'mrpack_Changelogger')
    os.makedirs(temp_dir, exist_ok=True)

    # unpack the .mrpack file into the temp directory
    if not path.endswith('.mrpack'):
        print('ERROR: Input file is not a .mrpack')
        sys.exit(1)
    with ZipFile(path, 'r') as zObject:
        zObject.extractall(path=temp_dir)

    # parse the json file
    try:
        with open(os.path.join(temp_dir, 'modrinth.index.json'), 'r', encoding="utf-8") as f:
            return json.load(f)
    except ValueError:
        print('ERROR: one modrinth.index.json is not formatted correctly')
        sys.exit(1)