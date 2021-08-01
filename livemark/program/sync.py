import sys
import typer
import difflib
from ..project import Project
from ..document import Document
from .main import program
from . import common


@program.command(name="sync")
def program_sync(
    source: str = common.source,
    print: bool = common.print,
    diff: bool = common.diff,
):
    """Sync the article."""

    try:

        # Create document
        document = Document(source, target=source, project=Project())

        # Process document
        document.process()

        # Diff document
        if diff:
            l1 = document.input.splitlines(keepends=True)
            l2 = document.output.splitlines(keepends=True)
            ld = list(difflib.unified_diff(l1, l2, fromfile="source", tofile="target"))
            if ld:
                typer.secho("".join(ld), nl=False)
                sys.exit(1)
            sys.exit(0)

        # Print document
        if print:
            document.print()
            sys.exit()

        # Write document
        document.write()

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
