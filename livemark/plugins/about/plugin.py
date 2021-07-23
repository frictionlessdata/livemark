from ...plugin import Plugin


class AboutPlugin(Plugin):
    def process_markup(self, markup):
        markup.query("head").append(self.read_asset("style.css"), tag="style")
        markup.query("#livemark-right").append(
            self.read_asset(
                "markup.html",
                data={
                    # TODO: make self.config available using "process_document/config"?
                    "description": markup.document.config.about.description,
                },
            )
        )
