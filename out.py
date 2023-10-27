def markdown_out(added_mods, removed_mods, updated_mods,):
    # Create the Markdown text
    markdown_text = ""

    if added_mods:
        markdown_text += f"\n# Added Mods\n\n{', '.join(added_mods)}\n"

    if removed_mods:
        markdown_text += f"# Removed Mods\n\n{', '.join(removed_mods)}\n"

    if updated_mods:
        markdown_text += f"\n# Updated Mods\n\n{', '.join(updated_mods)}\n"

    # Write the Markdown text to the output file
    with open("Changelog.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)
