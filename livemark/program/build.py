import typer
from ..project import Project
from ..document import Document
from .main import program
from . import common


@program.command(name="build")
def program_build(
    source: str = common.source,
    target: str = common.target,
    format: str = common.format,
    print: bool = common.print,
):
    """Build the article."""

    # Create document
    document = Document(
        source,
        target=target,
        format=format,
        project=Project(),
        create=True,
    )

    # Process document
    document.process()

    # Print document
    if print:
        document.print()
        raise typer.Exit()

    # Write document
    document.write()
