import os
import yaml
import deepmerge
import jsonschema
from copy import deepcopy
from .system import system
from .exception import LivemarkException


class Config(dict):
    def __init__(self, source):
        enable = []
        disable = []

        # Read config
        config = source or {}
        if not isinstance(config, dict):
            if os.path.isfile(config):
                with open(config) as file:
                    config = yaml.safe_load(file)

        # Process config
        for key, value in list(config.items()):
            if value is True:
                enable.append(key)
                del config[key]
            elif value is False:
                disable.append(key)
                del config[key]

        # Validate config
        for Plugin in system.combined:
            if config.get(Plugin.name) and Plugin.profile:
                validator = jsonschema.Draft7Validator(Plugin.profile)
                for error in validator.iter_errors(config[Plugin.name]):
                    message = f'Invalid "{Plugin.name}" config: {error.message}'
                    raise LivemarkException(message)

        # Set attributes
        self.update(config)
        self.__enable = enable
        self.__disable = disable

    @property
    def enable(self):
        return self.__enable

    @property
    def disable(self):
        return self.__disable

    # Helpers

    def merge(self, config):
        result = {}
        deepmerge.always_merger.merge(result, self)
        deepmerge.always_merger.merge(result, config)
        return Config(result)

    # Import/Export

    def to_copy(self):
        return deepcopy(self)

    def to_dict(self):
        return deepcopy(dict(self))
