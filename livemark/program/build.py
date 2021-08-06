import sys
import typer
from ..document import Document
from .main import program
from . import common


@program.command(name="build")
def program_build(
    source: str = common.source,
    target: str = common.target,
    format: str = common.format,
    config: str = common.config,
    print: bool = common.print,
    diff: bool = common.diff,
):
    """Build the processed article into a target file."""

    try:
        document = Document(source, target=target, format=format, config=config)
        written = document.build(diff=diff, print=print)
        if written and diff:
            sys.exit(1)
    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
