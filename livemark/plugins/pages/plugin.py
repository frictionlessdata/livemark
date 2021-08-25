from copy import deepcopy
from ...plugin import Plugin
from ... import helpers


# NOTE:
# Add animation for opening two-level menus
# Consider using gray background for menu items on hover (like in Docusaurus)


# TODO: fix tow-level menus on mobile!
# TODO: should we allow index pages for nested items (unlike in Docosaurus)?
# TODO: fix 2 line items
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

    def process_markup(self, markup):
        if self.items:
            markup.add_style("style.css")
            markup.add_script("script.js")
            markup.add_markup("markup.html", target="#livemark-left")
