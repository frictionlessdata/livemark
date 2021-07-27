import os
import typer
from .. import settings
from ..project import Project
from ..document import Document
from .main import program


@program.command(name="build")
def program_build(
    source: str = typer.Argument(settings.DEFAULT_PATH, help="Path to source"),
    target: str = typer.Option(None, help="Path to target"),
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
