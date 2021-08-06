import sys
import typer
from ..document import Document
from .main import program
from . import common


@program.command(name="sync")
def program_sync(
    source: str = common.source,
    config: str = common.config,
    print: bool = common.print,
    diff: bool = common.diff,
):
    """Sync the article."""

    try:
        document = Document(source, target=source, config=config)
        document.build(diff=diff, print=print)
    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
