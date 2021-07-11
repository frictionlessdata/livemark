import os
import typer
import difflib
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


# TODO: add an ability to build to markdown?
# TODO: add an ability to choose a target path?
@program.command(name="build")
def program_build(
    path: str = typer.Argument("index.md", help="Path to markdown"),
    print: bool = typer.Option(False, help="Return the document"),
):
    """Build the article."""

    # Process document
    document = Document(path)
    source, target = document.process_html()

    # Print document
    if print:
        typer.secho(target)
        raise typer.Exit()

    # Write document
    html_path = f"{os.path.splitext(path)[0]}.html"
    helpers.write_file(html_path, target)


@program.command(name="sync")
def program_sync(
    path: str = typer.Argument(..., help="Path to markdown"),
    diff: bool = typer.Option(default=False, help="Return the diff"),
    print: bool = typer.Option(default=False, help="Return the document"),
    version: Optional[bool] = typer.Option(None, "--version", callback=version),
):
    """Sync the article"""

    # Process document
    document = Document(path)
    source, target = document.process_markdown()

    # Diff document
    if diff:
        l1 = source.splitlines(keepends=True)
        l2 = target.splitlines(keepends=True)
        ld = list(difflib.unified_diff(l1, l2, fromfile="source", tofile="target"))
        typer.secho("".join(ld), nl=False)
        raise typer.Exit()

    # Print document
    if print:
        typer.secho(target)
        raise typer.Exit()

    # Write document
    helpers.write_file(path, target)


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
