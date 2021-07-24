import os
import typer
import difflib
from typing import Optional
from functools import partial
from livereload import Server
from .document import Document
from .project import Project
from . import settings


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
    """Livemark is a static site generator that extends Markdown with interactive charts, tables, scripts, and more."""
    pass


@program.command(name="build")
def program_build(
    source: str = typer.Argument(settings.DEFAULT_PATH, help="Path to source"),
    target: str = typer.Option(settings.DEFAULT_TARGET, help="Path to target"),
    print: bool = typer.Option(False, help="Return the document"),
):
    """Build the article."""

    # Create document
    if source == settings.DEFAULT_PATH:
        if not os.path.exists(source):
            with open(source, "w"):
                pass

    # Process document
    document = Document(source, target=target, project=Project())
    document.prepare()
    document.process()
    document.cleanup()

    # Print document
    if print:
        document.print()
        raise typer.Exit()

    # Write document
    document.write()


@program.command(name="sync")
def program_sync(
    source: str = typer.Argument(..., help="Path to markdown"),
    diff: bool = typer.Option(default=False, help="Return the diff"),
    print: bool = typer.Option(default=False, help="Return the document"),
    version: Optional[bool] = typer.Option(None, "--version", callback=version),
):
    """Sync the article"""

    # Process document
    document = Document(source, target=source, project=Project())
    document.prepare()
    document.process()
    document.cleanup()

    # Diff document
    if diff:
        l1 = document.input.splitlines(keepends=True)
        l2 = document.output.splitlines(keepends=True)
        ld = list(difflib.unified_diff(l1, l2, fromfile="source", tofile="target"))
        typer.secho("".join(ld), nl=False)
        raise typer.Exit()

    # Print document
    if print:
        document.print()
        raise typer.Exit()

    # Write document
    document.write()


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
