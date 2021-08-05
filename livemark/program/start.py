import sys
import typer
from livereload import Server
from ..document import Document
from ..project import Project
from .main import program
from . import common


@program.command(name="start")
def program_start(
    source: str = common.source,
    target: str = common.target,
    format: str = common.format,
):
    """Start a Livemark server."""

    try:

        # Build document
        def build():

            # Create document
            document = Document(
                source,
                target=target,
                format=format,
                project=Project(),
                create=True,
            )

            # Build document
            document.build()

        # Run server
        build()
        server = Server()
        server.watch(source, build, delay=1)
        server.serve(host="localhost", port=7000, root=".", open_url_delay=1)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
