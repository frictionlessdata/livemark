from ...plugin import Plugin


class LinksPlugin(Plugin):
    priority = 20

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            config=markup.plugin_config,
        )
