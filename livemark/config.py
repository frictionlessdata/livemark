import os
import yaml
import deepmerge
import jsonschema
from copy import deepcopy
from .exception import LivemarkException
from .system import system
from . import helpers


# NOTE:
# Make source to be only a file path to be trully file based (to use timestamps etc)


class Config(dict):
    def __init__(self, source):
        enable = []
        disable = []

        # Read config
        config = source or {}
        if not isinstance(config, dict):
            if os.path.isfile(config):
                config = yaml.safe_load(helpers.read_file(config))
            else:  # there is no config
                config = {}

        # Process config
        for key, value in list(config.items()):
            if value is True:
                enable.append(key)
                del config[key]
            elif value is False:
                disable.append(key)
                del config[key]

        # Validate config
        for Plugin in system.Plugins.values():
            if config.get(Plugin.code) and Plugin.profile:
                validator = jsonschema.Draft7Validator(Plugin.profile)
                for error in validator.iter_errors(config[Plugin.code]):
                    message = f'Invalid "{Plugin.code}" config: {error.message}'
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

    def to_copy(self):
        return deepcopy(self)

    def to_dict(self):
        return deepcopy(dict(self))

    def to_merge(self, source):
        result = {}
        deepmerge.always_merger.merge(result, self)
        deepmerge.always_merger.merge(result, source)
        for name in self.enable:
            result.setdefault(name, True)
        for name in self.disable:
            result.setdefault(name, False)
        return Config(result)
