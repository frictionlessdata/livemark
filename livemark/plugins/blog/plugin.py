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
    def process_project(project):
        if not project.document:
            path = project.config.get("blog", {}).get("path", "blog")
            if os.path.isdir(path):
                source = os.path.join(os.path.dirname(__file__), "index.md")
                target = os.path.join(path, "index.html")
                index = Document(source, target=target)
                project.documents.append(index)
                for source in glob.glob(f"{path}/**/*.md", recursive=True):
                    item = Document(source)
                    project.documents.append(item)
