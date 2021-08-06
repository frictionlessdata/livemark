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
    live: bool = common.live,
    host: str = common.host,
    port: str = common.port,
):
    """Merge Markdown file into itself."""

    try:

        # Create document
        document = Document(
            source,
            target=source,
            config=config,
        )

        # Normal mode
        if not live:
            written = document.build(diff=diff, print=print)
            if written and diff:
                sys.exit(1)
            sys.exit(0)

        # TODO: implement
        sys.exit(f"Live mode is not implemented: {host}:{port}")

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
