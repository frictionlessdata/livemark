import os
import inspect


class Plugin:
    def process_html(self, html):
        pass

    def process_snippet(self, snippet):
        pass

    def process_document(self, document):
        pass

    # Helpers

    def read_asset(self, *path):
        path = os.path.join([os.path.dirname(inspect.getfile(self.__class__)), *path])
        with open(path) as file:
            return file.read()
