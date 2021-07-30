from ...plugin import Plugin


class AboutPlugin(Plugin):
    priority = 30
    profile = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
        },
    }

    def process_markup(self, markup):
        if not self.config:
            return

        # Prepare context
        text = self.config.get("text", self.document.description)

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            text=text,
        )
