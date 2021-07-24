from ...plugin import Plugin


class BrandPlugin(Plugin):
    def process_markup(self, markup):
        config = markup.document.config.get("brand", {})
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("#livemark-left").append(
            self.read_asset("markup.html", config=config)
        )
