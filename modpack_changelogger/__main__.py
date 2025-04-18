#!/usr/bin/env python3
"""
Main entry point for running Modpack Changelogger as a module.

This allows the package to be imported in other Python scripts.
"""

from .cli_wrapper import main

if __name__ == "__main__":
    main()
