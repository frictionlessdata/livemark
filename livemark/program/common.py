from typer import Argument, Option
from .. import settings


# General


source = Argument(
    settings.DEFAULT_SOURCE,
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
    settings.DEFAULT_CONFIG,
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


# Command


diff = Option(
    default=False,
    help="Return the diff",
)

print = Option(
    False,
    help="Return the document",
)
