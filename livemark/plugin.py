import os
import inspect
import jsonschema
from jinja2 import Template
from .helpers import cached_property


class Plugin:
    profile = {}
    priority = 0

    @cached_property
    def name(self):
        return self.__class__.__name__.replace("Plugin", "").lower()

    # Actions

    def validate_document(self, document):
        if self.profile:
            jsonschema.validate(document.config.get(self.name), self.profile)

    def prepare_document(self, document):
        pass

    def process_document(self, document):
        pass

    def cleanup_document(self, document):
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
