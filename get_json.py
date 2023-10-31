def get_json (json_path):
    # Load the old and new packs
    with open(json_path, 'r', encoding="utf-8") as f:
        return json_path.json.load(f)
