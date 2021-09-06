import os
import sys
import typer
from ..project import Project
from ..server import Server
from .main import program
from .. import settings
from .. import helpers
from . import common


# NOTE:
# We need to improve the default template by making it faster and more informative


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
            if not source:
                source = settings.DEFAULT_SOURCE
                if not os.path.exists(source):
                    helpers.copy_file(settings.TEMPLATE, source)

        # Create project
        project = Project(
            source,
            target=target,
            format=format,
            config=config,
        )

        # Live mode
        server = Server(project)
        server.start(host=host, port=port)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
