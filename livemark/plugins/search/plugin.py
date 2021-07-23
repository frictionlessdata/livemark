from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_html(self, markup):
        markup.query("#livemark-main").append(self.read_asset("markup.html"))
