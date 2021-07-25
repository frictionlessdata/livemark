import typer
from functools import partial
from livereload import Server
from .build import program_build
from .main import program
from .. import settings


@program.command(name="start")
def program_start(
    source: str = typer.Argument("index.md", help="Path to markdown"),
    target: str = typer.Option(settings.DEFAULT_TARGET, help="Path to target"),
):
    """Start a Livemark server."""
    program_build(source, target, False)
    server = Server()
    server.watcher.watch(".", delay=1)
    server.watch(source, partial(program_build, source, target, False))
    server.serve(host="localhost", port=7000, root=".", open_url_delay=1)
