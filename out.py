import sys

def markdown_out(added, removed, updated, config):
    style = config['format']['style']

    if style == "bullet_list":
        markdown_text = bullet_list(added, removed, updated)
    elif style == "comma_list":
        markdown_text = comma_list(added, removed, updated)
    elif style == "ind_bullet_list":
        markdown_text = ind_bullet_list(added, removed, updated)
    elif style == "ind_comma_list":
        markdown_text = ind_comma_list(added, removed, updated)
    else:
        print("Warning: Invalid style specified in config.json, using bullet_list as a fallback.")
        markdown_text = bullet_list(added, removed, updated)

    try:
        with open(config['output']['file_path'] + config['output']['file_name'], "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except FileNotFoundError:
        print("Error: The folder specified in config.json doesn't exist.")
        sys.exit(1)
    except PermissionError:
        print("Error: You don't have access to the folder specified in config.json. Try running as administrator")
        sys.exit(1)

def bullet_list(added, removed, updated):
    markdown_text = ""

    if added:
        markdown_text += "## Added\n"
        for mod in added:
            markdown_text += f"- {mod}\n"

    if removed:
        markdown_text += "## Removed\n"
        for mod in removed:
            markdown_text += f"- {mod}\n"

    if updated:
        markdown_text += "## Updated\n"
        for mod in updated:
            markdown_text += f"- {mod}\n"

    return markdown_text

def comma_list(added, removed, updated):
    markdown_text = ""

    if added:
        markdown_text += "* Added: "
        for mod in added:
            markdown_text += f"{mod}, "

    if removed:
        markdown_text += "\n* Removed: "
        for mod in removed:
            markdown_text += f"{mod}, "

    if updated:
        markdown_text += "\n* Updated: "
        for mod in updated:
            markdown_text += f"{mod}, "

    return markdown_text

def ind_bullet_list(added, removed, updated):
    markdown_text = ""
    markdown_text += "Changes: "
    if added:
        for mod in added:
            markdown_text += f"\n* added {mod}"

    if removed:
        for mod in removed:
            markdown_text += f"\n* removed {mod}"

    if updated:
        for mod in updated:
            markdown_text += f"\n* updated {mod}"

    return markdown_text

def ind_comma_list(added, removed, updated):
    markdown_text = ""
    markdown_text += "Changes: "
    if added:
        for mod in added:
            markdown_text += f"added {mod}, "

    if removed:
        for mod in removed:
            markdown_text += f"removed {mod}, "

    if updated:
        for mod in updated:
            markdown_text += f"updated {mod}, "

    return markdown_text