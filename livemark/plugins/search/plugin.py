from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        markup.add_markup(
            "markup.html",
            target="#livemark-main",
        )
