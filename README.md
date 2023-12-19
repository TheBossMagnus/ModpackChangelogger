# MrpackChangelogger
MrpackChangelogger is a Python tool that compares two Minecraft Modpacks (in .mrpack format) and generates a markdown changelog to show the difference between tham.


## Features
- **Precise Comparison**: Easily spot added, removed, and modified items, changes to the Minecraft version, and updates to modloaders.
- **Markdown Output**: View the differences in a markdown document with style options.
- **Configurability**: You can customize output through a config file.
- **Multi-Platform**: Run it on Windows or Linux, no Python installation required.

## Installation
You can find the complied windows(.exe) and linux versions in the latest release.
Or you can also run it with the python interpreter:
```bash
python MrpackChangelogger.py [args]
```

## Basic Usage

You can run MrpackChangelogger from the command line with the following arguments:

- `-o`, `--old`: Specify the first pack to compare.
- `-n`, `--new`: Specify the pack to compare  against.
- `-c`, `--config`: Use a config file; 'new' creates a new one.
- `-f`, `--file`: Specify the output file for the markdown file.
- `-d`, `--debug`: Enable debug logging (output to `log.txt`).

> Note that that the only mandatory command is -n when -o is specified and viceversa

E.g:Compare `old_pack` to `new_pack` using the settings in `config.json`, and write the output to `output.md`.
```bash
python MrpackChangelogger -o old_pack -n new_pack -c config.json -f output.md
```

## Limitations
* As now just the .mrpack format is supported, CourseForge support is coming soon
* Mod added as .jar file(overrides) aren't checked

>This is my first time using python seriosuly, so if you have any suggestion about code quality or performance feel free to pr them! And if something is broken sorry, open an issue and will do my best to fix it.