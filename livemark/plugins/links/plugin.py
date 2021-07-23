from ...plugin import Plugin


class LinksPlugin(Plugin):
    def process_html(self, markup):
        config = markup.document.config
        markup.query("head").append(self.read_asset("style.css"))
        markup.query("#livemark-right").append(
            self.read_asset("markup.html"), items=config.links.items
        )
