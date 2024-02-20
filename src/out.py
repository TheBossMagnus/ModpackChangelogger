import logging
import sys

def markdown_out(added, removed, updated, old_info, new_info, config, changelog_file):
    style = config['format']['style']
    available_styles = {
        "bullet": bullet_list,
        "comma": comma_list,
        "ind_bullet": ind_bullet_list,
        "ind_comma": ind_comma_list
    }
    markdown_text = []
    markdown_text.append(generate_header(old_info, new_info, config))
    markdown_text = available_styles.get(style, bullet_list)(added, removed, updated, markdown_text)

    if changelog_file is None:
        changelog_file = "Changelog.md"
    if changelog_file.lower()  == "console":
        print(markdown_text)
        return

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

def generate_header(old_info, new_info, config):
    header = ""
    if not config['format']['header']['header']:
        return header

    name = config['format']['header'].get('Name')
    if name == 'Auto':
        name = new_info['modpack_name']

    header += f"{'#' * config['format']['header']['size']} {name}" if name else ""
    if config['format']['header'].get('ShowOld version'):
        header += f" {old_info['modpack_version']} =>"
    if config['format']['header'].get('ShowNew version'):
        header += f" {new_info['modpack_version']}"
    return header + "\n"

def bullet_list(added, removed, updated, markdown_text):

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

def comma_list(added, removed, updated, markdown_text):

    if added:
        markdown_text.append(f"- **Added:** {', '.join(added)}")
    if removed:
        markdown_text.append(f"- **Removed:** {', '.join(removed)}")
    if updated:
        markdown_text.append(f"- **Updated:** {', '.join(updated)}")

    return '\n'.join(markdown_text)

def ind_bullet_list(added, removed, updated, markdown_text):

    if added:
        markdown_text.append('\n'.join(f"* Added {mod}" for mod in added))
    if removed:
        markdown_text.append('\n'.join(f"* Removed {mod}" for mod in removed))
    if updated:
        markdown_text.append('\n'.join(f"* Updated {mod}" for mod in updated))

    return '\n'.join(markdown_text)

def ind_comma_list(added, removed, updated, markdown_text):
    markdown_text.append("**Changes:**")

    if added:
        markdown_text.append(', '.join(f"Added {mod}" for mod in added))
    if removed:
        markdown_text.append(', '.join(f"Removed {mod}" for mod in removed))
    if updated:
        markdown_text.append(', '.join(f"Updated {mod}" for mod in updated))

    return ' '.join(markdown_text)