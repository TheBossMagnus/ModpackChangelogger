#!/usr/bin/env python3
"""
Main entry point for running ModpackChangelogger as a module.

This allows the package to be run as:
python -m modpack_changelogger
"""

from .cli_wrapper import main

if __name__ == "__main__":
    main()
