import importlib
import frictionless
from jinja2 import Environment, FileSystemLoader
from ...plugin import Plugin


class LogicPlugin(Plugin):
    identity = "logic"
    priority = 90

    # Context

    @property
    def context(self):
        context = {}
        context["document"] = self.document
        context["livemark"] = importlib.import_module("livemark")
        context["frictionless"] = frictionless
        return context

    # Process

    def process_document(self, document):
        environ = Environment(loader=FileSystemLoader("."), trim_blocks=True)
        template = environ.from_string(document.content)
        document.content = template.render(**self.context)
