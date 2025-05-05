# This file is a CLI wrapper for the modpack_changelogger function in main.py
# It provides a CLI interface for the package

import aiohttp
import click

from .main import generate_changelog
from .utils import (
    ConfigValidationError,
    DifferentModpackFormatError,
    ModpackFormatError,
    UnsupportedModpackFormatError,
    create_config,
)
from .version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "-?"])


def handle_error(error, message=None):
    """Centralized error handler for CLI errors."""
    if message:
        click.echo(f"Error: {message}", err=True)
        click.echo(f"Details: {error}", err=True)
    else:
        click.echo(f"Error: {error}", err=True)


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("-v", "--version", is_flag=True, help="Show the version and exit")
@click.option("-o", "--old", help="First pack to compare")
@click.option("-n", "--new", help="The pack to compare against")
@click.option("-c", "--config", help="Use a config file")
@click.option("-f", "--file", help="Specify the output file for the changelog")
def cli(version, old, new, config, file):
    """CLI wrapper for Modpack Changelogger."""
    if version:
        click.echo(f"Modpack Changelogger {__version__}")
        return

    if not (old and new):
        handle_error(
            RuntimeError(
                "Both old and new modpacks must be provided for the comparison."
            )
        )
        return

    try:
        generate_changelog(old, new, config, file)
        click.echo(f"Changelog successfully generated in '{file}'.")
    except FileNotFoundError as error:
        handle_error(error)
    except PermissionError as error:
        handle_error(error)
    except (
        TimeoutError,
        aiohttp.ClientConnectionError,
        aiohttp.ClientResponseError,
    ) as error:
        handle_error(
            error,
            "Unable to connect to the API. Please check your internet connection and try again.",
        )
    except (
        UnsupportedModpackFormatError,
        DifferentModpackFormatError,
        ModpackFormatError,
        ConfigValidationError,
    ) as error:
        handle_error(error, getattr(error, "message", None))
    except Exception as error:
        handle_error(error, "Unhandled error.")


@cli.command(context_settings=CONTEXT_SETTINGS)
def newconfig():
    """Create a new configuration file."""
    try:
        create_config()
        click.echo("A new configuration file has been created successfully.")
    except Exception as error:
        handle_error(error, "Unable to create a new configuration file.")


if __name__ == "__main__":
    cli()
