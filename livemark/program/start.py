import typer
from functools import partial
from livereload import Server
from .build import program_build
from .main import program


@program.command(name="start")
def program_start(
    source: str = typer.Argument("index.md", help="Path to markdown"),
    target: str = typer.Option(None, help="Path to target"),
    format: str = typer.Option(None, help="Format of the target file"),
):
    """Start a Livemark server."""
    # TODO: rebase on using Document instead of the program call
    program_build(source, target, format, False)
    server = Server()
    server.watcher.watch(".", delay=1)
    server.watch(source, partial(program_build, source, target, format, False))
    server.serve(host="localhost", port=7000, root=".", open_url_delay=1)
