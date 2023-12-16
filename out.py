import sys
import logging

def markdown_out(added, removed, updated, config, changelog_file):
    style = config['format']['style']
    available_styles = {
        "bullet": bullet_list,
        "comma": comma_list,
        "ind_bullet": ind_bullet_list,
        "ind_comma": ind_comma_list
    }
    markdown_text = available_styles.get(style, bullet_list)(added, removed, updated)

    try:
        with open(changelog_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)
            logging.debug("Created %s", changelog_file)
    except FileNotFoundError:
        logging.error("ERROR: The folder selected for the changelog (%s) doesn't exist.", changelog_file)
        sys.exit(1)
    except PermissionError:
        logging.error("ERROR: You don't have access to the folder specified in config.json (%s). Try running as administrator", config['output']['file_path'])
        sys.exit(1)


def bullet_list(added, removed, updated):
    markdown_text = []

    if added:
        markdown_text.append("###  Added:")
        markdown_text.extend([f"- {mod}" for mod in added])
    if removed:
        markdown_text.append("###  Removed:")
        markdown_text.extend([f"- {mod}" for mod in removed])
    if updated:
        markdown_text.append("### Updated:")
        markdown_text.extend([f"- {mod}" for mod in updated])

    return '\n'.join(markdown_text)

def comma_list(added, removed, updated):
    markdown_text = []

    if added:
        markdown_text.append(f"- **Added:** {', '.join(added)}")
    if removed:
        markdown_text.append(f"- **Removed:** {', '.join(removed)}")
    if updated:
        markdown_text.append(f"- **Updated:** {', '.join(updated)}")

    return '\n'.join(markdown_text)

def ind_bullet_list(added, removed, updated):
    markdown_text = ["## Changes:"]

    if added:
        markdown_text.append('\n'.join(f"* Added {mod}" for mod in added))
    if removed:
        markdown_text.append('\n'.join(f"* Removed {mod}" for mod in removed))
    if updated:
        markdown_text.append('\n'.join(f"* Updated {mod}" for mod in updated))

    return '\n'.join(markdown_text)

def ind_comma_list(added, removed, updated):
    markdown_text = ["**Changes:**"]

    if added:
        markdown_text.append(', '.join(f"Added {mod}" for mod in added))
    if removed:
        markdown_text.append(', '.join(f"Removed {mod}" for mod in removed))
    if updated:
        markdown_text.append(', '.join(f"Updated {mod}" for mod in updated))

    return ' '.join(markdown_text)