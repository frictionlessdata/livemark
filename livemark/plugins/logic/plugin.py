import importlib
import frictionless
from jinja2 import Environment, FileSystemLoader
from ...plugin import Plugin


class LogicPlugin(Plugin):
    code = "logic"
    priority = 90

    # Process

    def process_document(self, document):
        livemark = importlib.import_module("livemark")
        templating = Environment(loader=FileSystemLoader("."), trim_blocks=True)
        template = templating.from_string(document.content)
        document.content = template.render(
            document=document,
            livemark=livemark,
            frictionless=frictionless,
        )
