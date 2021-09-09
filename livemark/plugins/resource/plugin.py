import yaml
from ...plugin import Plugin
from frictionless import Resource


# NOTE:
# We need to render description's markdown


class ResourcePlugin(Plugin):
    identity = "resource"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "resource" and snippet.lang == "yaml":
                spec = yaml.safe_load(str(snippet.input).strip())
                self.__count += 1
                resource = Resource(**spec)
                snippet.output = self.read_asset("markup.html", resource=resource) + "\n"
