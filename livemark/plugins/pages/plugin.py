from pathlib import Path
from copy import deepcopy
from ...plugin import Plugin
from ...document import Document


# TODO: improve two-level menus!
# TODO: fix tow-level menus on mobile!
# TODO: rebase sidebars on using background on hover instead of color
# TODO: should we allow index pages for nested items (unlike in Docosaurus)?
# TODO: review paths format - md/html?
# TODO: fix 2 line items
class PagesPlugin(Plugin):
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
        current = "/"
        if self.document.target != "index.html":
            current = f"/{self.document.target}"
        return current

    @Plugin.property
    def items(self):
        items = deepcopy(self.config["items"])
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
        return flatten(self.items)

    # Process

    @classmethod
    def process_project(cls, project):
        items = project.config.get("pages", {}).get("items", [])
        for item in flatten(items):
            source = str(Path(item["path"]).with_suffix(".md"))
            document = Document(source, project=project)
            project.documents.append(document)

    def process_markup(self, markup):
        if self.config:
            markup.add_style("style.css")
            markup.add_script("script.js")
            markup.add_markup(
                "markup.html",
                target="#livemark-left",
                items=self.items,
            )


# Internal


def flatten(items):
    flatten_items = []
    for item in items:
        subitems = item.get("items", [])
        for subitem in subitems:
            flatten_items.append(subitem)
        if not subitems:
            flatten_items.append(item)
    return flatten_items
