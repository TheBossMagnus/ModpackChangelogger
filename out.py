def markdown_out(added_mods, removed_mods, updated_mods, config):

    if config['format']['style'] == "comma":
        markdown_text = comma_list(added_mods, removed_mods, updated_mods)
    elif config['format']['style']  == "bullet":
        markdown_text = bullet_list(added_mods, removed_mods, updated_mods)
    else:
        markdown_text = bullet_list(added_mods, removed_mods, updated_mods)

    # Write the Markdown text to the output file
    with open("Changelog.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

def bullet_list(added_mods, removed_mods, updated_mods,):
    markdown_text = ""

    if added_mods:
        markdown_text += f"## Added Mods\n"
        for mod in added_mods:
            markdown_text += f"- {mod}\n"

    if removed_mods:
        markdown_text += f"## Removed Mods\n"
        for mod in removed_mods:
            markdown_text += f"- {mod}\n"

    if updated_mods:
        markdown_text += f"## Updated Mods\n"
        for mod in updated_mods:
            markdown_text += f"- {mod}\n"

    return markdown_text

def comma_list(added_mods, removed_mods, updated_mods,):
    markdown_text = ""

    if added_mods:
        markdown_text += f"* Added: "
        for mod in added_mods:
            markdown_text += f"{mod}, "

    if removed_mods:
        markdown_text += f"\n* Removed: "
        for mod in removed_mods:
            markdown_text += f"{mod}, "

    if updated_mods:
        markdown_text += f"\n* Updated: "
        for mod in updated_mods:
            markdown_text += f"{mod}, "

    return markdown_text