import sys
import typer
import atexit
import tempfile
from ..server import Server
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

        # Live mode
        atexit.register(document.build)
        with tempfile.NamedTemporaryFile(suffix=".html") as file:
            mirror = Document(source, target=file.name)
            server = Server(mirror)
            server.start(host=host, port=port, file=file.name)

    except Exception as exception:
        raise
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
