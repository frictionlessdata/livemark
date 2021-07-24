from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        markup.query("#livemark-main").append(self.read_asset("markup.html"))
