import typer
from .. import settings
from typing import Optional


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
    """Livemark is a static site generator
    that extends Markdown with interactive charts, tables, scripts, and more.
    """
    pass
