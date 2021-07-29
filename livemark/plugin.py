import os
import inspect
from jinja2 import Template
from .helpers import cached_property


class Plugin:
    priority = 0
    profile = None

    @cached_property
    def name(self):
        return self.__class__.__name__.replace("Plugin", "").lower()

    # Actions

    def process_document(self, document):
        pass

    def process_snippet(self, snippet):
        pass

    def process_markup(self, markup):
        pass

    # Helpers

    def get_config(self, object, *, plugin=None):
        document = getattr(object, "document", object)
        return document.config.get(plugin or self.name)

    def read_asset(self, *path, **context):
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        with open(path) as file:
            text = file.read().strip()
        if context:
            template = Template(text, trim_blocks=True)
            text = template.render(**context)
        return text
