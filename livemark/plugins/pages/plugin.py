from ...plugin import Plugin


class PagesPlugin(Plugin):
    priority = 80
    profile = {
        "type": "object",
        "properties": {
            "items": {
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

    def process_config(self, config):
        if self.config:
            self.config.setdefault("items", self.config.pop("self", []))

    def process_markup(self, markup):
        if not self.config:
            return

        # Prepare context
        current = "/"
        if self.document.target != "index.html":
            current = f"/{self.document.target}"
        items = self.config["items"]

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
            current=current,
            items=items,
        )
