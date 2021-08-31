import importlib
import frictionless
from jinja2 import Environment, FileSystemLoader
from ...plugin import Plugin


class LogicPlugin(Plugin):
    code = "logic"
    priority = 90

    # Process

    @staticmethod
    def process_project(project):
        livemark = importlib.import_module("livemark")
        project.context["livemark"] = livemark
        project.context["frictionless"] = frictionless

    def process_document(self, document):
        project = self.document.project
        environ = Environment(loader=FileSystemLoader("."), trim_blocks=True)
        template = environ.from_string(document.content)
        document.content = template.render(document=document, **project.context)
