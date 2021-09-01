import os
import yaml
import deepmerge
import jsonschema
from copy import deepcopy
from .system import system
from . import helpers
from . import errors


# NOTE:
# Make source to be only a file path to be trully file based (to use timestamps etc)
# Allow applying config dict on top of the file-based source?


class Config(dict):
    """Livemark config

    API      | Usage
    -------- | --------
    Public   | `from livemark import Config`

    Parameters:
        source (str): path to the config source

    """

    def __init__(self, source):
        enabled = []
        disabled = []

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
                enabled.append(key)
                del config[key]
            elif value is False:
                disabled.append(key)
                del config[key]

        # Validate config
        for Plugin in system.Plugins.values():
            if config.get(Plugin.identity) and Plugin.validity:
                validator = jsonschema.Draft7Validator(Plugin.validity)
                for error in validator.iter_errors(config[Plugin.identity]):
                    message = f'Invalid "{Plugin.identity}" config: {error.message}'
                    raise errors.Error(message)

        # Set attributes
        self.update(config)
        self.__enabled = enabled
        self.__disabled = disabled

    # Plugins

    @property
    def enabled(self):
        """List of enabled plugin names

        Returns:
            str[]: plugin names
        """
        return self.__enabled

    @property
    def disabled(self):
        """List of disabled plugin names

        Returns:
            str[]: plugin names
        """
        return self.__disabled

    # Helpers

    def to_copy(self):
        """Create a copy

        Returns:
            Config: config copy
        """
        return deepcopy(self)

    def to_dict(self):
        """Create a dict

        Returns:
            dict: config dict
        """
        return deepcopy(dict(self))

    def to_merge(self, source):
        """Create a merge

        Parameters:
            source (dict): dictionary to merge

        Returns:
            Config: config merge
        """
        result = {}
        deepmerge.always_merger.merge(result, self)
        deepmerge.always_merger.merge(result, source)
        for name in self.enabled:
            result.setdefault(name, True)
        for name in self.disabled:
            result.setdefault(name, False)
        return Config(result)
