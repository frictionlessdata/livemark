from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        if not self.config:
            return

        # Update markup
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
        )
