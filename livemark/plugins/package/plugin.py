import json
import yaml
from ...plugin import Plugin
from frictionless import Package


# NOTE:
# We need to render description's markdown


class PackagePlugin(Plugin):
    identity = "package"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "package" and snippet.lang in ["yaml", "json"]:
                if snippet.lang == "yaml":
                    spec = yaml.safe_load(str(snippet.input).strip())
                if snippet.lang == "json":
                    spec = json.loads(str(snippet.input).strip())
                self.__count += 1
                package = Package(**spec)
                snippet.output = self.read_asset("markup.html", package=package) + "\n"
