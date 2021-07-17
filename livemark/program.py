import os
import typer
import difflib
from typing import Optional
from functools import partial
from livereload import Server
from .document import Document
from . import settings
from . import helpers


# Program

program = typer.Typer()


# Helpers


def version(value: bool):
    if value:
        typer.echo(settings.VERSION)
        raise typer.Exit()


# Command


@program.callback()
def program_main(
    version: Optional[bool] = typer.Option(None, "--version", callback=version)
):
    """Publish articles written in extended Markdown at ease."""
    pass


# TODO: add an ability to build to markdown?
@program.command(name="build")
def program_build(
    source: str = typer.Argument(settings.DEFAULT_PATH, help="Path to source"),
    target: str = typer.Option(settings.DEFAULT_TARGET, help="Path to target"),
    print: bool = typer.Option(False, help="Return the document"),
):
    """Build the article."""

    # TODO: review
    # Create document
    if source == settings.DEFAULT_PATH:
        if not os.path.exists(source):
            with open(source, "w"):
                pass

    # Process document
    document = Document(source, target=target)
    document.prepare()
    document.process()
    document.cleanup()

    # Print document
    if print:
        typer.secho(document.target)
        raise typer.Exit()

    # Write document
    if document.target:
        helpers.write_file(document.target, document.output)


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
    typer.secho(settings.LAYOUT)
