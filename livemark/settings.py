from . import helpers


# General


VERSION = helpers.read_asset("VERSION")
TEMPLATE = helpers.path_asset("documents", "template.md")


# Defaults


DEFAULT_SOURCE = "index.md"
DEFAULT_FORMAT = "html"
DEFAULT_CONFIG = "livemark.yaml"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 7000
DEFAULT_FILE = "index.html"
