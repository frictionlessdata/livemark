import jsonschema
from ...plugin import Plugin
from ...system import system


class ConfigPlugin(Plugin):
    priority = 50

    def process_document(self, document):

        # Normalize config
        for key, value in document.config.items():
            if value is True:
                document.config[key] = {"value": True}

        # Validate config
        for name, plugin in system.plugins.items():
            plugin_config = document.config.get(name)
            if plugin_config is not None and plugin.profile is not None:
                jsonschema.validate(plugin_config, plugin.profile)
