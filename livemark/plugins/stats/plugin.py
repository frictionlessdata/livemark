from ...plugin import Plugin


class StatsPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-left").append(self.read_asset("markup.html"))
