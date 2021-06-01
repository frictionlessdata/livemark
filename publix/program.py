import typer
import difflib
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


@program.command()
def program_main(
    path: str = typer.Argument(..., help="Path to markdown"),
    diff: bool = typer.Option(default=False, help="Return the diff"),
    print: bool = typer.Option(default=False, help="Return the document"),
    version: Optional[bool] = typer.Option(None, "--version", callback=version),
):
    """Publish articles written in extended Markdown at ease."""

    # Process document
    document = Document(path)
    source, target = document.process()

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
