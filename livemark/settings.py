import os


# Helpers


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "assets", *paths)) as file:
        return file.read().strip()


# General


VERSION = read_asset("VERSION")
DEFAULT_PATH = "index.md"
DEFAULT_CONFIG_PATH = "livemark.yaml"
LAYOUT = read_asset("templates", "layout.html")
UNDEFINED = object()
DEFAULT_TARGET = "index.html"
