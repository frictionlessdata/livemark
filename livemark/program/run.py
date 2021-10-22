import os
import sys
import typer
from ..project import Project
from .main import program
from .. import settings
from . import common


# NOTE:
# It's an initial implementation that works directly with markdown renderer
# We need to implement it properly using a normal system flow


@program.command(name="run")
def program_run(
    run_id: str = common.run_id,
    list: bool = common.list,
    config: str = common.config,
):
    """Run a Livemark script(s)."""

    try:

        # Handle config
        if not config:
            if os.path.exists(settings.DEFAULT_CONFIG):
                config = settings.DEFAULT_CONFIG

        # Create project
        project = Project(config=config)
        project.read()
        project.process()
        for document in project.documents:
            document.read()
            print(document.content)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
