from ...plugin import Plugin


class BrandPlugin(Plugin):
    def process_html(self, html):
        html("#livemark-left").append(self.read_asset("markup.html"))
