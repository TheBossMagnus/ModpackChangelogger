import sys

def markdown_out(added, removed, updated, config):
    def format_changes(changes, prefix, separator):
        return prefix + separator.join(changes)

    style_config = {
        "comma": {"prefixes": {"added": "* Added: ", "removed": "\n* Removed: ", "updated": "\n* Updated: "}, "separator": ", "},
        "bullet": {"prefixes": {"added": "## Added\n- ", "removed": "## Removed\n- ", "updated": "## Updated\n- "}, "separator": "\n- "},
        "ind_bullet": {"prefixes": {"added": "\n* added ", "removed": "\n* removed ", "updated": "\n* updated "}, "separator": "\n* "},
        "ind_comma": {"prefixes": {"added": "added ", "removed": "removed ", "updated": "updated "}, "separator": ", "}
    }

    style = config['format']['style']
    style_config = style_config.get(style, style_config["bullet"])

    markdown_text = "Changes: " if "ind" in style else ""
    if added:
        markdown_text += format_changes(added, style_config["prefixes"]["added"], style_config["separator"]) + "\n"
    if removed:
        markdown_text += format_changes(removed, style_config["prefixes"]["removed"], style_config["separator"]) + "\n"
    if updated:
        markdown_text += format_changes(updated, style_config["prefixes"]["updated"], style_config["separator"]) + "\n"

    try:
        with open(config['output']['file_path'] + config['output']['file_name'], "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except FileNotFoundError:
        print("Error: The folder specified in config.json doesn't exist.")
        sys.exit(1)
    except PermissionError:
        print("Error: You don't have access to the folder specified in config.json. Try running as administrator")
        sys.exit(1)