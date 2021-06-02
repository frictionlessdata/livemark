import os
import typer
from typing import Optional
from .document import Document
from . import helpers
from . import config


# Program

program = typer.Typer()


# Helpers


def version(value: bool):
    if value:
        typer.echo(config.VERSION)
        raise typer.Exit()


# Command


@program.callback()
def program_main(
    version: Optional[bool] = typer.Option(None, "--version", callback=version)
):
    """Publish articles written in extended Markdown at ease."""
    pass


@program.command(name="build")
def program_build(
    path: str = typer.Argument("index.md", help="Path to markdown"),
    print: bool = typer.Option(False, help="Return the document"),
):
    """Build and article."""

    # Process document
    document = Document(path)
    source, target = document.process()

    # Print document
    if print:
        typer.secho(target)
        raise typer.Exit()

    # Write document
    html_path = f"{os.path.splitext(path)[0]}.html"
    helpers.write_file(html_path, target)
