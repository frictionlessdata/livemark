import deepmerge
import jsonschema
from copy import deepcopy
from .system import system
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

    def __init__(self, mapping):
        enabled = []
        disabled = []

        # Process config
        for key, value in list(mapping.items()):
            if value is True:
                enabled.append(key)
                del mapping[key]
            elif value is False:
                disabled.append(key)
                del mapping[key]

        # Validate config
        for Plugin in system.Plugins.values():
            if mapping.get(Plugin.identity) and Plugin.validity:
                validator = jsonschema.Draft7Validator(Plugin.validity)
                for error in validator.iter_errors(mapping[Plugin.identity]):
                    message = f'Invalid "{Plugin.identity}" config: {error.message}'
                    raise errors.Error(message)

        # Set attributes
        self.update(mapping)
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

    def to_merge(self, mapping):
        """Create a merge

        Parameters:
            mapping (dict): dictionary to merge

        Returns:
            Config: config merge
        """
        this = {}
        deepmerge.always_merger.merge(this, self)
        deepmerge.always_merger.merge(this, mapping)
        for name in self.enabled:
            this.setdefault(name, True)
        for name in self.disabled:
            this.setdefault(name, False)
        return Config(this)
