from ...plugin import Plugin


class StatusPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-right").append(self.read_asset("markup.html"))
