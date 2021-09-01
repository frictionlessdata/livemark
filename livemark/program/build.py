import os
import sys
import typer
from ..server import Server
from ..project import Project
from ..document import Document
from .main import program
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

        # Validate project
        if not os.path.exists(config):
            if not source:
                message = 'Project without config requires "source" argument'
                raise errors.Error(message)

        # Create project
        document = None
        if source:
            document = Document(source, target=target, format=format)
        project = Project(document, config=config, format=format)

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
