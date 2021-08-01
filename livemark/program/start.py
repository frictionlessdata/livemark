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

        # Create process
        def process():

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

            # Write document
            document.write()

        # Run server
        process()
        server = Server()
        server.watcher.watch(".", delay=1)
        server.watch(source, process)
        server.serve(host="localhost", port=7000, root=".", open_url_delay=1)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
