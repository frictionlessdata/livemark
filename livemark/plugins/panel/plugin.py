from ...plugin import Plugin


# TODO: add scroll to markup
class PanelPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-right").append(self.read_asset("markup.html"))
