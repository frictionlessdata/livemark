from ...plugin import Plugin


class TocPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-left").append(self.read_asset("markup.html"))
