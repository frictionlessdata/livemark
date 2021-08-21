from ...plugin import Plugin


class AboutPlugin(Plugin):
    priority = 20
    profile = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def text(self):
        return self.config.get("text", self.document.description)

    # Process

    def process_markup(self, markup):
        if self.config:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-right",
                # TODO: pass self as "plugin" automatically (in all plugins)?
                text=self.text,
            )
