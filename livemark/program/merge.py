import os
import sys
import typer
import atexit
import tempfile
from ..server import Server
from ..project import Project
from ..document import Document
from .main import program
from .. import errors
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

        # Validate project
        if not os.path.exists(config):
            if not source:
                message = 'Project without config requires "source" argument'
                raise errors.Error(message)

        # Create project
        project = Project(
            source,
            format="md",
            config=config,
        )

        # Normal mode
        if not live:
            output = project.build(diff=diff, print=print)
            if output and diff:
                sys.exit(1)
            sys.exit(0)

        # Live mode
        if not project.document:
            message = 'Live mode requries the "source" argument'
            raise errors.Error(message)
        atexit.register(project.document.build)
        with tempfile.NamedTemporaryFile(suffix=".html") as file:
            server = Server(Document(source, target=file.name).project)
            server.start(host=host, port=port, file=file.name)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
