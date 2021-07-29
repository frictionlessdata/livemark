import os
import inspect
import jsonschema
from jinja2 import Template
from .exception import LivemarkException


# TODO: implement process_config hook?
class Plugin:
    priority = 0
    profile = {}

    def __init__(self, document):
        self.__document = document

        # Normalize/validate config
        config = document.config.setdefault(self.name, {})
        if config is True:
            document.config[self.name] = {"value": config}
        if config and self.profile:
            jsonschema.validate(config, self.profile)

    @property
    def name(self):
        return self.__class__.__name__.replace("Plugin", "").lower()

    @property
    def document(self):
        return self.__document

    @property
    def config(self):
        return self.__document.config[self.name]

    # Actions

    def process_document(self, document):
        pass

    def process_snippet(self, snippet):
        pass

    def process_markup(self, markup):
        pass

    # Helpers

    def get_plugin(self, name):
        for plugin in self.document.plugins:
            if plugin.name == name:
                return plugin
        raise LivemarkException(f"Pluin is not registered: {name}")

    def read_asset(self, *path, **context):
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        with open(path) as file:
            text = file.read().strip()
        if context:
            template = Template(text, trim_blocks=True)
            text = template.render(**context)
        return text
