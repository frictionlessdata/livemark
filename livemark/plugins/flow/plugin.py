from ...plugin import Plugin


class FlowPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-main").append(self.read_asset("markup.html"))
