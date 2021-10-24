import importlib
import frictionless
from jinja2 import Environment, FileSystemLoader
from ...plugin import Plugin


class LogicPlugin(Plugin):
    identity = "logic"
    priority = 80

    def __init__(self, document):
        super().__init__(document)

        # Prepare context
        self.__context = {}
        self.__context["document"] = self.document
        self.__context["livemark"] = importlib.import_module("livemark")
        self.__context["frictionless"] = frictionless

    # Context

    @property
    def context(self):
        return self.__context

    # Process

    def process_document(self, document):
        environ = Environment(loader=FileSystemLoader("."), trim_blocks=True)
        template = environ.from_string(document.content)
        document.content = template.render(**self.context)
