import sys

def format_changes(added, removed, updated, style):
    actions = [("Added", added), ("Removed", removed), ("Updated", updated)]
    
    if style == 'bullet':
        return "\n".join([f"## {title}\n" + "\n".join(f"- {mod}" for mod in mods) for title, mods in actions if mods])
    elif style == 'comma':
        return "\n".join([f"* **{title}**: " + ", ".join(mod for mod in mods) for title, mods in actions if mods])
    elif style == 'ind_bullet':
        return "Changes:\n" + "\n".join([f"* {action} {mod}" for action, mods in actions for mod in mods])
    elif style == 'ind_comma':
        return "**Changes:** " + ", ".join([f"{action} {mod}" for action, mods in actions for mod in mods])
    else:
        raise ValueError(f"Invalid style: {style}")

def markdown_out(added, removed, updated, config):
    style = config['format']['style']
    markdown_text = format_changes(added, removed, updated, style)

    try:
        with open(config['output']['file_path'] + config['output']['file_name'], "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except FileNotFoundError:
        print("Error: The folder specified in config.json doesn't exist.")
        sys.exit(1)
    except PermissionError:
        print("Error: You don't have access to the folder specified in config.json. Try running as administrator")
        sys.exit(1)