import os
import sys
import typer
from ..server import Server
from ..project import Project
from .main import program
from .. import settings
from .. import errors
from . import common


# NOTE:
# Live mode always opens index file even though another source is provided


@program.command(name="build")
def program_build(
    source: str = common.source,
    target: str = common.target,
    format: str = common.format,
    config: str = common.config,
    print: bool = common.print,
    diff: bool = common.diff,
    live: bool = common.live,
    host: str = common.host,
    port: str = common.port,
):
    """Build Markdown file into HTML by default."""

    try:

        # Handle config
        if not config:
            if os.path.exists(settings.DEFAULT_CONFIG):
                config = settings.DEFAULT_CONFIG

        # Handle source
        if not source and not config:
            if os.path.exists(settings.DEFAULT_SOURCE):
                source = settings.DEFAULT_SOURCE

        # Validate project
        if not source and not config:
            message = 'Project without "source" requires "config"'
            raise errors.Error(message)

        # Create project
        project = Project(
            source,
            target=target,
            format=format,
            config=config,
        )

        # Normal mode
        if not live:
            output = project.build(diff=diff, print=print)
            if output and diff:
                sys.exit(1)
            sys.exit(0)

        # Live mode
        server = Server(project)
        server.start(host=host, port=port)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
