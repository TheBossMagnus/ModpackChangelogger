def markdown_out(added, removed, updated, config):

    if config['format']['style'] == "comma":
        markdown_text = comma_list(added, removed, updated)
    elif config['format']['style']  == "bullet":
        markdown_text = bullet_list(added, removed, updated)
    else:
        markdown_text = bullet_list(added, removed, updated)

    # Write the Markdown text to the output file
    with open("Changelog.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

def bullet_list(added, removed, updated):
    markdown_text = ""

    if added:
        markdown_text += f"## Added\n"
        for mod in added:
            markdown_text += f"- {mod}\n"

    if removed:
        markdown_text += f"## Removed\n"
        for mod in removed:
            markdown_text += f"- {mod}\n"

    if updated:
        markdown_text += f"## Updated\n"
        for mod in updated:
            markdown_text += f"- {mod}\n"

    return markdown_text

def comma_list(added, removed, updated):
    markdown_text = ""

    if added:
        markdown_text += f"* Added: "
        for mod in added:
            markdown_text += f"{mod}, "

    if removed:
        markdown_text += f"\n* Removed: "
        for mod in removed:
            markdown_text += f"{mod}, "

    if updated:
        markdown_text += f"\n* Updated: "
        for mod in updated:
            markdown_text += f"{mod}, "

    return markdown_text