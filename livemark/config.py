import yaml
import deepmerge
import jsonschema
from copy import deepcopy
from .system import system
from . import helpers
from . import errors


class Config(dict):
    """Livemark config

    API      | Usage
    -------- | --------
    Public   | `from livemark import Config`

    Parameters:
        source (str): path to the config source

    """

    def __init__(self, source=None):
        status = {}

        # Load config
        if isinstance(source, str):
            self.update(yaml.safe_load(helpers.read_file(source)))
        elif source:
            self.update(source)
            source = None

        # Process config
        for key, value in list(self.items()):
            if isinstance(value, bool):
                status[key] = value
                del self[key]

        # Validate config
        for Plugin in system.Plugins.values():
            if self.get(Plugin.identity) and Plugin.validity:
                validator = jsonschema.Draft7Validator(Plugin.validity)
                for error in validator.iter_errors(self[Plugin.identity]):
                    message = f'Invalid "{Plugin.identity}" config: {error.message}'
                    raise errors.Error(message)

        # Set attributes
        self.__source = source
        self.__status = status

    @property
    def source(self):
        """Path of the config source

        Returns:
            str?: source
        """
        return self.__source

    @property
    def status(self):
        """Mapping of plugin status

        Returns:
            dict<bool>: status
        """
        return self.__status

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
        source = {}
        deepmerge.always_merger.merge(source, self)
        deepmerge.always_merger.merge(source, mapping)
        for key, value in self.status.items():
            source[key] = value
        return Config(source)
