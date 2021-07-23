import os
import inspect
from jinja2 import Template


class Plugin:
    def process_markup(self, markup):
        pass

    def process_snippet(self, snippet):
        pass

    def process_document(self, document):
        pass

    # Helpers

    def read_asset(self, *path, tag=None, data=None):
        path = os.path.join([os.path.dirname(inspect.getfile(self.__class__)), *path])
        with open(path) as file:
            text = file.read()
        if tag:
            text = f"<{tag}>\n{text}\n</{tag}>"
        if data:
            template = Template(text)
            text = template.render(data=data)
        return text
