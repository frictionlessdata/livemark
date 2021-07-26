import typer
import difflib
from ..project import Project
from ..document import Document
from .main import program


@program.command(name="sync")
def program_sync(
    source: str = typer.Argument(..., help="Path to markdown"),
    diff: bool = typer.Option(default=False, help="Return the diff"),
    print: bool = typer.Option(default=False, help="Return the document"),
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
