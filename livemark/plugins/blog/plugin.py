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

    # Process

    @staticmethod
    def process_project(project):
        if not project.document:
            path = project.config.get("blog", {}).get("path", "blog")
            if os.path.isdir(path):
                source_default = os.path.join(os.path.dirname(__file__), "index.md")
                source = os.path.join(path, "index.md")
                if not os.path.isfile(source):
                    helpers.copy_file(source_default, source)
                for source in glob.glob(f"{path}/**/*.md", recursive=True):
                    item = Document(source)
                    project.documents.append(item)
