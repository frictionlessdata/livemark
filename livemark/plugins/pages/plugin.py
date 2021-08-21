from copy import deepcopy
from ...plugin import Plugin


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
            "list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
                        "list": {"type": "array"},
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
        items = deepcopy(self.config["list"])
        for item in items:
            item["active"] = False
            subitems = item.get("list", [])
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
    def items_flatten(self):
        items = []
        for item in self.items:
            subitems = item.get("list", [])
            for subitem in subitems:
                items.append(subitem)
            if not subitems:
                items.append(item)
        return items

    # Process

    def process_config(self, config):
        if self.config:
            self.config.setdefault("list", self.config.pop("self", []))

    def process_markup(self, markup):
        if self.config:
            markup.add_style("style.css")
            markup.add_script("script.js")
            markup.add_markup(
                "markup.html",
                target="#livemark-left",
                items=self.items,
            )
