from ...plugin import Plugin


class SearchPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-main").append(self.read_asset("markup.html"))
