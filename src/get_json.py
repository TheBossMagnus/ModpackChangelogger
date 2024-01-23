import json
import logging
import os
import shutil
import sys
from zipfile import ZipFile


def get_json(path):
    # Ensure the file is a modpack file
    if not path.endswith('.mrpack'):
        logging.error('ERROR: Input file is not a modpack')
        sys.exit(1)
    if not os.path.exists(path):
        logging.error('ERROR: The file %s does not exist', path)
        sys.exit(1)

    # Create a temporary directory
    temp_dir = os.path.join(os.environ.get('TEMP'), 'ModpackChangelogger')
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Unpack the modpack file into the temp directory
        with ZipFile(path, 'r') as zip_obj:
            zip_obj.extractall(path=temp_dir)
            logging.debug('Extracted %s to %s', path, temp_dir)

        # Parse the json file
        json_path = os.path.join(temp_dir, 'modrinth.index.json')
        with open(json_path, 'r', encoding="utf-8") as json_file:
            logging.debug('Parsed %s', json_path)
            return json.load(json_file)
    except FileNotFoundError:
        logging.error('ERROR: The file %s does not exist', json_path)
        sys.exit(1)
    except ValueError:
        logging.error('ERROR: The file %s is not formatted correctly', json_path)
        sys.exit(1)
    finally:
        # Delete the extracted files
        shutil.rmtree(temp_dir)
        logging.debug('Deleted the temp files in %s', temp_dir)