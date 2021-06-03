import os


# Helpers


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "assets", *paths)) as file:
        return file.read().strip()


# General


VERSION = read_asset("VERSION")
TEMPLATES = os.path.join(os.path.dirname(__file__), "assets", "templates")
LAYOUT = read_asset("templates", "layout.html")
TABLE = read_asset("templates", "table.html")
CHART = read_asset("templates", "chart.html")
