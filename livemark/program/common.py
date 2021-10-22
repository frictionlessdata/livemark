from typer import Argument, Option
from .. import settings


# General


source = Argument(
    None,
    help="Path to the source file",
)

target = Option(
    None,
    help="Path to the target file",
)

format = Option(
    None,
    help="Format of the target file",
)

config = Option(
    None,
    help="Path to a config file",
)

host = Option(
    settings.DEFAULT_HOST,
    help="Server host",
)

port = Option(
    settings.DEFAULT_PORT,
    help="Server port",
)

run = Argument(
    None,
    help="A run id",
)

list = Option(
    default=False,
    help="List available run ids",
)


# Command


live = Option(
    default=False,
    help="Live mode",
)


diff = Option(
    default=False,
    help="Return the diff",
)

print = Option(
    False,
    help="Return the document",
)
