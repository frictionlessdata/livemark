import os
import sys
import typer
from ..project import Project
from ..document import Document
from ..server import Server
from .main import program
from .. import settings
from .. import helpers
from . import common


# NOTE:
# We can bootstrap source with some examplar content
# showing Livemark's features and ready for editiing


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

        # Bootstrap project
        if not os.path.exists(config):
            source = source or settings.DEFAULT_SOURCE
            if not not os.path.exists(source):
                helpers.write_file(source)

        # Create project
        document = None
        if source:
            document = Document(source, target=target, format=format)
        project = Project(document, config=config, format=format)

        # Live mode
        server = Server(project)
        server.start(host=host, port=port)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
