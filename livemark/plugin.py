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

    code = ""
    priority = 0
    profile = {}
    property = cached_property

    def __init__(self, document):
        self.__document = document

    @property
    def config(self):
        return self.__document.config.get(self.code, {})

    @property
    def document(self):
        return self.__document

    # Actions

    @staticmethod
    def process_project(project):
        pass

    def process_document(self, document):
        pass

    def process_snippet(self, snippet):
        pass

    def process_markup(self, markup):
        pass

    # Helpers

    @classmethod
    def get_type(cls):
        if cls.__module__.startswith("livemark_"):
            return "external"
        return "internal"

    def read_asset(self, *path, **context):
        project = self.document.project
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        context.update(project.context)
        context["plugin"] = self
        with open(path) as file:
            template = Template(file.read().strip(), trim_blocks=True)
            text = template.render(**context)
        return text
