from ...plugin import Plugin


class AboutPlugin(Plugin):
    def process_markup(self, markup):
        config = markup.document.config
        markup.query("head").append(self.read_asset("style.css"), tag="style")
        markup.query("#livemark-right").append(
            self.read_asset("markup.html", description=config.about.description)
        )
