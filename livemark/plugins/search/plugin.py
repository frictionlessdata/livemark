from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        config = self.get_config(markup)
        if not config:
            return

        # Update markup
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
        )
