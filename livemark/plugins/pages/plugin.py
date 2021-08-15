from ...plugin import Plugin


class PagesPlugin(Plugin):
    priority = 80
    profile = {
        "type": "object",
        "properties": {
            "list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
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
        return self.config["list"]

    @Plugin.property
    def items_flatten(self):
        items = []
        for item in self.items:
            subitems = item.get("list", [])
            if not subitems:
                items.append(item)
                continue
            for subitem in subitems:
                items.append(subitem)
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
                current=self.current,
                items=self.items,
            )
