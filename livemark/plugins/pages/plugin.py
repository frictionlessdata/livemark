from ...plugin import Plugin


class PagesPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-left").append(self.read_asset("markup.html"))
