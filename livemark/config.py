import os


# Helpers


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "assets", *paths)) as file:
        return file.read().strip()


# General


VERSION = read_asset("VERSION")
TEMPLATES = os.path.join(os.path.dirname(__file__), "assets", "templates")
# TODO: rebase fully on Jinja's directory loader
LAYOUT = read_asset("templates", "layout.html")
TABLE = read_asset("templates", "features", "table.html")
CHART = read_asset("templates", "features", "chart.html")
