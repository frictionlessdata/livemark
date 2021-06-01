import os


# Helpers


def read_asset(*paths):
    dirname = os.path.dirname(__file__)
    return open(os.path.join(dirname, "assets", *paths)).read().strip()


# General


VERSION = read_asset("VERSION")
