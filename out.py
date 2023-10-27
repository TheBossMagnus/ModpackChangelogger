def print_mods_to_markdown(added_mods, updated_mods, removed_mods):
    # Create the Markdown text
    markdown_text = ""

    if added_mods[0]:
        markdown_text += f"\n# Added Mods\n\n{', '.join(added_mods[0])}\n"

    if removed_mods[0]:
        markdown_text += f"# Removed Mods\n\n{', '.join(removed_mods[0])}\n"

    if updated_mods[0]:
        markdown_text += f"\n# Updated Mods\n\n{', '.join(updated_mods[0])}\n"

    # Write the Markdown text to the output file
    with open("Changelog.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)
