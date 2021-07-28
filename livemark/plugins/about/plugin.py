from ...plugin import Plugin


class AboutPlugin(Plugin):
    priority = 30

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare context
        description = markup.plugin_config.get("description", markup.document.description)

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            description=description,
        )
