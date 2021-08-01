import os
import yaml
from . import settings


class Project:
    """Livemark project

    API      | Usage
    -------- | --------
    Public   | `from livemark import Project`

    Parameters:
        path? (str): a project path

    """

    def __init__(self, path=""):
        self.__path = path

        # Read config
        self.__config = {}
        config_path = os.path.join(path, settings.DEFAULT_CONFIG_PATH)
        if os.path.isfile(config_path):
            with open(config_path) as file:
                self.__config = yaml.safe_load(file)

    @property
    def path(self):
        return self.__path

    @property
    def config(self):
        return self.__config
