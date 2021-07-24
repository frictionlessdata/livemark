from ...plugin import Plugin


class StatusPlugin(Plugin):
    def process_markup(self, markup):
        config = markup.document.config.get("status", {})
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("#livemark-right").append(
            self.read_asset("markup.html", config=config)
        )
