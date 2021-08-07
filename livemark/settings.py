import os


# Helpers


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "assets", *paths)) as file:
        return file.read().strip()


# General


VERSION = read_asset("VERSION")
DEFAULT_SOURCE = "index.md"
DEFAULT_FORMAT = "html"
DEFAULT_CONFIG = "livemark.yaml"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 7000
DEFAULT_FILE = "index.html"
UNDEFINED = object()
