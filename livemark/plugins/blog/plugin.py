import os
import glob
from ...plugin import Plugin
from ...document import Document
from ... import helpers


class BlogPlugin(Plugin):
    name = "blog"
    profile = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def path(self):
        path = self.document.project.config.get("blog", {}).get("path", "blog")
        if os.path.isdir(path):
            return path

    @Plugin.property
    def items(self):
        items = []
        if not self.path:
            return items
        index_path = os.path.join(self.path, "index")
        for document in self.document.project.documents:
            if document.path.startswith(self.path) and document.path != index_path:
                items.append({"document": document})
        return items

    # Process

    @staticmethod
    def process_project(project):
        if not project.document:
            path = project.config.get("blog", {}).get("path", "blog")
            if os.path.isdir(path):
                index_default = os.path.join(os.path.dirname(__file__), "index.md")
                index_source = os.path.join(path, "index.md")
                if not os.path.isfile(index_source):
                    helpers.copy_file(index_default, index_source)
                for source in glob.glob(f"{path}/**/*.md", recursive=True):
                    if source != index_source:
                        item = Document(source)
                        project.documents.append(item)
