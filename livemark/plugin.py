import os
import inspect
from jinja2 import Template
from .helpers import cached_property


class Plugin:
    """Livemark plugin

    API      | Usage
    -------- | --------
    Public   | `from livemark import Plugin`

    Parameters:
        document (Document): a document to which the plulgin belongs

    """

    property = cached_property
    priority = 0
    profile = {}

    def __init__(self, document):
        self.__document = document
        self.process_plugin()

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

    def process_plugin(self):
        pass

    def process_config(self, config):
        pass

    def process_document(self, document):
        pass

    def process_snippet(self, snippet):
        pass

    def process_markup(self, markup):
        pass

    # Helpers

    def read_asset(self, *path, **context):
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        with open(path) as file:
            text = file.read().strip()
        if context:
            template = Template(text, trim_blocks=True)
            text = template.render(**context)
        return text
