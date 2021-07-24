from ...plugin import Plugin


class PagesPlugin(Plugin):
    def process_html(self, markup):
        config = markup.document.config.get("links", {})
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("#livemark-left").append(
            self.read_asset("markup.html", config=config)
        )
