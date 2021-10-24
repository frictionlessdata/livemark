import os
import glob
from ...plugin import Plugin
from ...document import Document
from ... import helpers


class BlogPlugin(Plugin):
    identity = "blog"
    validity = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
        },
    }

    # Context

    @property
    def path(self):
        path = self.document.project.config.get("blog", {}).get("path", "blog")
        if os.path.isdir(path):
            return path

    @property
    def relpath(self):
        path = f"{self.path}/index.html"
        return helpers.get_relpath(path, self.document.path)

    @property
    def items(self):
        items = []
        if not self.path:
            return items
        index_path = "/".join([self.path, "index"])
        for document in self.document.project.documents:
            if document.path.startswith(self.path) and document.path != index_path:
                relpath = helpers.get_relpath(document.path, self.document.path)
                items.append({"document": document, "relpath": relpath})
        return items

    @property
    def author(self):
        return self.config.get("author")

    @property
    def image(self):
        return self.config.get("image")

    @property
    def date(self):
        if self.path:
            date = self.document.path.replace(f"{self.path}/", "")
            return "-".join(date.split("-")[:3])

    # Process

    @staticmethod
    def process_project(project):
        path = project.config.get("blog", {}).get("path", "blog")
        if os.path.isdir(path):
            index_default = os.path.join(os.path.dirname(__file__), "index.md")
            index_source = os.path.join(path, "index.md")
            if not os.path.isfile(index_source):
                helpers.copy_file(index_default, index_source)
            for source in glob.glob(f"{path}/**/*.md", recursive=True):
                if source != index_source:
                    item = Document(source, project=project)
                    project.documents.append(item)

    def process_markup(self, markup):
        markup.add_style("style.css")
        if self.author:
            markup.add_markup("markup.html", target="h1 + p", action="prepend")
            markup.query('a[href="/blog/index.html"]').parent().add_class("active")
