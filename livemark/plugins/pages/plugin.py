from copy import deepcopy
from ...plugin import Plugin
from ...document import Document
from ... import helpers


# NOTE:
# Consider using animation for opening two-level menus


class PagesPlugin(Plugin):
    name = "pages"
    priority = 70
    profile = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name"],
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

    @Plugin.property
    def current(self):
        return self.document.path

    @Plugin.property
    def items(self):
        items = deepcopy(self.config.get("items", []))
        for item in items:
            item["active"] = False
            subitems = item.get("items", [])
            for subitem in subitems:
                subitem["active"] = False
                if subitem["path"] == self.current:
                    item["active"] = True
                    subitem["active"] = True
            if not subitems:
                if item["path"] == self.current:
                    item["active"] = True
        return items

    @Plugin.property
    def flatten_items(self):
        return helpers.flatten_items(self.items, "items")

    # Process

    @staticmethod
    def process_project(project):
        items = project.config.get("pages", {}).get("items", [])
        for item in helpers.flatten_items(items, "items"):
            source = helpers.with_format(item["path"], "md")
            target = helpers.with_format(item["path"], project.format)
            document = Document(source, target=target, name=item["name"])
            project.documents.append(document)

    def process_markup(self, markup):
        if self.items:
            markup.add_style("style.css")
            markup.add_script("script.js")
            markup.add_markup("markup.html", target="#livemark-left")
