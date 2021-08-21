import frictionless
from jinja2 import Environment, FileSystemLoader
from ...plugin import Plugin


class LogicPlugin(Plugin):
    priority = 90

    # Process

    def process_document(self, document):
        templating = Environment(loader=FileSystemLoader("."), trim_blocks=True)
        template = templating.from_string(document.content)
        document.content = template.render(frictionless=frictionless)
