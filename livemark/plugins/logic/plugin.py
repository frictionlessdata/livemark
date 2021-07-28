import frictionless
from jinja2 import Environment, FileSystemLoader
from ...plugin import Plugin


class LogicPlugin(Plugin):
    priority = 40

    def process_document(self, document):
        templating = Environment(loader=FileSystemLoader("."), trim_blocks=True)
        template = templating.from_string(document.input)
        document.input = template.render(frictionless=frictionless)
