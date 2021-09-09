#  import yaml
from ...plugin import Plugin


class NotebookPlugin(Plugin):
    identity = "notebook"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "notebook" and snippet.lang == "yaml":
                #  spec = yaml.safe_load(str(snippet.input).strip())
                self.__count += 1
                snippet.output = self.read_asset("markup.html") + "\n"
