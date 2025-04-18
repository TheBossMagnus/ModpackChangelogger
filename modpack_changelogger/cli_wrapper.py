# This file is a CLI wrapper for the modpack_changelogger function in main.py
# It provides a CLI interface for the package
import click
import sys

from .main import generate_changelog
from .version import __version__
from .utils import ConfigValidationError, DifferentModpackFormatError, ModpackFormatError, UnsupportedModpackFormatError, create_config


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "-?"])


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
    if old and new:
        # Generate changelog directly from top-level command
        try:
            generate_changelog(old, new, config, file)
            click.echo(f"Changelog successfully generated in '{file}'!")
        except FileNotFoundError as e:
            click.echo(f"ERROR: {e}", err=True)
            raise click.Abort()
        except PermissionError as e:
            click.echo(f"ERROR: Unable to create or access the file '{e.filename}'. Please check file permissions.", err=True)
            raise click.Abort()
        except UnsupportedModpackFormatError as e:
            click.echo(f"ERROR: {e}", err=True)
            raise click.Abort()
        except DifferentModpackFormatError as e:
            click.echo(f"ERROR: {e}", err=True)
            raise click.Abort()
        except ModpackFormatError as e:
            click.echo(f"ERROR: {e}", err=True)
            raise click.Abort()
        except ConfigValidationError as e:
            click.echo(f"ERROR: The configuration file is worngly formatted: {e}", err=True)
            raise click.Abort()
        except Exception as e:
            click.echo(f"UNHANDLED ERROR: {e}", err=True)
            raise click.Abort()
    elif not sys.argv[1:]:
        click.echo(cli.get_help(click.get_current_context()))
        sys.exit(0)
    elif old or new:
        # If only one of old or new is provided
        click.echo("ERROR: Both --old and --new options are required for changelog generation", err=True)
        sys.exit(1)


@cli.command(context_settings=CONTEXT_SETTINGS)
def newconfig():
    """Create a new configuration file."""
    try:
        create_config()
        click.echo("A new configuration file has been created successfully")
    except Exception as e:
        click.echo(f"ERROR: Unable to create a new configuration file: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
