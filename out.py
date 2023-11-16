import sys

def markdown_out(added, removed, updated, config):
    style = config['format']['style']
    available_styles = {
        "bullet_list": bullet_list,
        "comma_list": comma_list,
        "ind_bullet_list": ind_bullet_list,
        "ind_comma_list": ind_comma_list
    }

    # Get the funct based on the style in the config, use bullet_list as a fallback
    markdown_text = available_styles.get(style, bullet_list)(added, removed, updated)

    try:
        with open(config['output']['file_path'] + config['output']['file_name'], "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except FileNotFoundError:
        print("ERROR: The folder specified in config.json doesn't exist.")
        sys.exit(1)
    except PermissionError:
        print("ERROR: You don't have access to the folder specified in config.json. Try running as administrator")
        sys.exit(1)

def bullet_list(added, removed, updated):
    markdown_text = ""

    if added:
        markdown_text += "# Added\n"
        for mod in added:
            markdown_text += f"- {mod}\n"

    if removed:
        markdown_text += "# Removed\n"
        for mod in removed:
            markdown_text += f"- {mod}\n"

    if updated:
        markdown_text += "# Updated\n"
        for mod in updated:
            markdown_text += f"- {mod}\n"

    return markdown_text

def comma_list(added, removed, updated):
    markdown_text = ""

    if added:
        markdown_text += "* **Added:** "
        for mod in added:
            markdown_text += f"{mod}, "

    if removed:
        markdown_text += "\n* **Removed:** "
        for mod in removed:
            markdown_text += f"{mod}, "

    if updated:
        markdown_text += "\n* **Updated:** "
        for mod in updated:
            markdown_text += f"{mod}, "

    return markdown_text

def ind_bullet_list(added, removed, updated):
    markdown_text = ""
    markdown_text += "# Changes: "
    if added:
        for mod in added:
            markdown_text += f"\n* Added {mod}"

    if removed:
        for mod in removed:
            markdown_text += f"\n* Removed {mod}"

    if updated:
        for mod in updated:
            markdown_text += f"\n* Updated {mod}"

    return markdown_text

def ind_comma_list(added, removed, updated):
    markdown_text = ""
    markdown_text += "**Changes:** "
    if added:
        for mod in added:
            markdown_text += f"Added {mod}, "

    if removed:
        for mod in removed:
            markdown_text += f"Removed {mod}, "

    if updated:
        for mod in updated:
            markdown_text += f"Updated {mod}, "

    return markdown_text