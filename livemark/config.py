import os
import yaml
import jsonschema
from .system import system
from .exception import LivemarkException


class Config(dict):
    def __init__(self, source):

        # Process config
        config = source or {}
        if not isinstance(config, dict):
            if os.path.isfile(config):
                with open(config) as file:
                    config = yaml.safe_load(file)

        # Validate config
        for Plugin in system.Plugins:
            if config.get(Plugin.name) and Plugin.profile:
                validator = jsonschema.Draft7Validator(Plugin.profile)
                for error in validator.iter_errors(config[Plugin.name]):
                    message = f'Invalid "{Plugin.name}" config: {error.message}'
                    raise LivemarkException(message)

        # Store config
        self.update(config)
