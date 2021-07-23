from ...plugin import Plugin


class StatusPlugin(Plugin):
    def process_html(self, markup):
        config = markup.document.config
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("#livemark-left").append(
            self.read_asset(
                "markup.html",
                user=config.status.user,
                repo=config.status.repo,
                type=config.status.type,
            )
        )
