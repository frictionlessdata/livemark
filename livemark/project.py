import os
import yaml


class Project:
    def __init__(self, *, config=None):

        # Normalize config
        config = config or {}
        if not isinstance(config, dict):
            if os.path.isfile(config):
                with open(config) as file:
                    config = yaml.safe_load(file)

        # Set attributes
        self.__config = config

    @property
    def config(self):
        return self.__config
