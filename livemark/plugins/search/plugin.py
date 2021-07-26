from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Update markup
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
        )
