import sys
import typer
from ..document import Document
from .main import program
from . import common


@program.command(name="merge")
def program_merge(
    source: str = common.source,
    config: str = common.config,
    print: bool = common.print,
    diff: bool = common.diff,
):
    """Merge the processed article into the same file."""

    try:
        document = Document(source, target=source, config=config)
        document.build(diff=diff, print=print)
    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
