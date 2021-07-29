from ...plugin import Plugin


class AboutPlugin(Plugin):
    priority = 30
    profile = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
        },
    }

    def process_markup(self, markup):
        config = self.get_config(markup)
        if not config:
            return

        # Prepare context
        description = config.get("description", markup.document.description)

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            description=description,
        )
