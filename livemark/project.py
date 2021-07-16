import os
import yaml
from .config import Config
from . import settings


class Project:
    def __init__(self, path=""):
        self.__path = path

        # Read config
        self.__config = Config()
        config_path = os.path.join(path, settings.CONFIG_PATH)
        if os.path.isfile(config_path):
            with open(config_path) as file:
                self.__config = Config(yaml.safe_load(file))

    @property
    def path(self):
        return self.__path

    @property
    def config(self):
        return self.__config
