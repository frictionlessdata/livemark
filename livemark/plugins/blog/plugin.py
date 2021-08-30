import os
import glob
from ...plugin import Plugin
from ...document import Document


class BlogPlugin(Plugin):
    name = "blog"
    profile = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "date": {"type": "string"},
        },
    }

    # Process

    @staticmethod
    def process_project(self, project):
        path = project.config.get("blog", {}).get("path", "blog")
        if os.path.isfile(path):

            # Add index
            source = os.path.join(os.path.dirname(__file__), "index.md")
            target = os.path.join(path, "index.html")
            index = Document(source, target=target)
            project.documents.append(index)

            # Add items
            for source in glob.glob(f"{self.path}/**/*.md"):
                item = Document(source)
                project.documents.append(item)

    def process_markup(self, markup):
        pass
