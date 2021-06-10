import os
import typer
from typing import Optional
from functools import partial
from livereload import Server
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


@program.command(name="start")
def program_start(
    path: str = typer.Argument("index.md", help="Path to markdown"),
):
    """Start a Livemark server."""
    program_build(path, False)
    server = Server()
    server.watcher.watch(".", delay=1)
    server.watch(path, partial(program_build, path, False))
    server.serve(host="localhost", port=7000, root=".", open_url_delay=1)


@program.command(name="layout")
def program_layout():
    """Print default layout."""
    typer.secho(config.LAYOUT)
