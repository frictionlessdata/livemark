import os
import sys
import typer
from ..project import Project
from ..document import Document
from ..server import Server
from .main import program
from .. import helpers
from . import common


# TODO: add cosole logging to build/start
@program.command(name="start")
def program_start(
    source: str = common.source,
    target: str = common.target,
    format: str = common.format,
    config: str = common.config,
    host: str = common.host,
    port: str = common.port,
):
    """Start a Livemark server."""

    try:

        # Create source
        if not os.path.exists(source):
            helpers.write_file(source)

        # Create project
        project = Project(config=config)

        # Create document
        document = Document(
            source,
            target=target,
            format=format,
            project=project,
        )

        # Run server
        server = Server(document)
        server.start(host=host, port=port)

    except Exception as exception:
        raise
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
