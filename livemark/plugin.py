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

    @property
    def name(self):
        return self.__class__.get_name()

    @property
    def config(self):
        return self.__document.config.get(self.name, {})

    @property
    def document(self):
        return self.__document

    # Actions

    def process_document(self, document):
        pass

    def process_snippet(self, snippet):
        pass

    def process_markup(self, markup):
        pass

    # Helpers

    # TODO: review naming "name"/function
    @classmethod
    def get_name(cls):
        return cls.__name__.replace("Plugin", "").lower()

    def read_asset(self, *path, **context):
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        with open(path) as file:
            text = file.read().strip()
        if context:
            template = Template(text, trim_blocks=True)
            text = template.render(**context)
        return text
