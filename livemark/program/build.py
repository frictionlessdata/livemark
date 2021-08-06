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
):
    """Build the processed article into a different file."""

    try:
        document = Document(source, target=target, format=format, config=config)
        document.build(print=print)
    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
