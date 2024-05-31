# ModpackChangelogger
ModpackChangelogger is a Python tool that compares two Minecraft Modpacks (in modrinth.mrpack or curseforge.zip format) and generates a markdown changelog to show the difference between them.


## Features
- **Precise Comparison**: Easily spot added, removed, and modified items, changes to the Minecraft version, and updates to modloaders.
- **Markdown Output**: View the differences in a markdown document with various [styles](https://github.com/TheBossMagnus/ModpackChangelogger/wiki/Configuration#format-section) options.
- **Configurability**: You can customize output through a [config file](https://github.com/TheBossMagnus/ModpackChangelogger/wiki/Configuration).
- **Multi-Platform**: Run it on Windows or Linux, Python installation not mandatory.

## Installation
Install the pip package
```bash
pip install modpack-changelogger
```
Or use the compiled windows `.exe`.
More information [on the wiki](https://github.com/TheBossMagnus/ModpackChangelogger/wiki/Install-and-run).
## Basic Usage
- `-o`, `--old`: Specify the first pack to compare.
- `-n`, `--new`: Specify the pack to compare  against.

E.g:Compare `old_pack` to `new_pack` using the settings in `config.json`, and write the output to `output.md`.
```bash
python ModpackChangelogger -o old_pack -n new_pack -c config.json -f output.md
```
More information [on the wiki](https://github.com/TheBossMagnus/ModpackChangelogger/wiki/Commands).
