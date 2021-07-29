from ...plugin import Plugin


class BrandPlugin(Plugin):
    priority = 100
    profile = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
        },
    }

    def process_markup(self, markup):
        config = self.get_config(markup)
        if not config:
            return

        # Prepare context
        title = config.get("title", markup.document.title)

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
            title=title,
        )
