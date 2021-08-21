from ...plugin import Plugin


class BrandPlugin(Plugin):
    priority = 80
    profile = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def text(self):
        return self.config.get("text", self.document.title)

    # Process

    def process_markup(self, markup):
        if self.config:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-left",
                text=self.text,
            )
