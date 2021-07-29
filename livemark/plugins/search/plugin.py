from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        config = markup.document.config.get(self.name, {})
        if not config:
            return

        # Update markup
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
        )
