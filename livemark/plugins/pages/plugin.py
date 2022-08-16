from copy import deepcopy
from ...plugin import Plugin
from ...document import Document
from ... import helpers


class PagesPlugin(Plugin):
    identity = "pages"
    priority = 70
    validity = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
                        "items": {"type": "array"},
                    },
                },
            },
        },
    }

    # Context

    @property
    def current(self):
        return self.document.path

    @property
    def items(self):
        items = deepcopy(self.config.get("items", []))
        for item in items:
            item["active"] = False
            subitems = item.get("items", [])

            # Handle nested
            for subitem in subitems:
                document = self.document.project.get_document(subitem["path"])
                subitem.setdefault("name", document.get_plugin("site").name)
                subitem["active"] = False
                subitem["relpath"] = helpers.get_url_relpath(
                    subitem["path"], self.current
                )
                if subitem["path"] == self.current:
                    item["active"] = True
                    subitem["active"] = True

            # Handle top-level
            if not subitems:
                document = self.document.project.get_document(item["path"])
                item.setdefault("name", document.get_plugin("site").name)
                item["relpath"] = helpers.get_url_relpath(item["path"], self.current)
                if item["path"] == self.current:
                    item["active"] = True

        return items

    @property
    def flatten_items(self):
        return helpers.flatten_items(self.items, "items")

    # Process

    @staticmethod
    def process_project(project):
        items = project.config.get("pages", {}).get("items", [])
        for item in helpers.flatten_items(items, "items"):
            source = item.get("from", helpers.with_format(item["path"], "md"))
            target = helpers.with_format(item["path"], project.format)
            document = Document(source, target=target, project=project, path=item["path"])
            project.documents.append(document)

    def process_markup(self, markup):
        if self.items:
            markup.add_style("style.css")
            markup.add_script("script.js")
            markup.add_markup("markup.html", target="#livemark-left")
