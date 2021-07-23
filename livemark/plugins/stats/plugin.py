import datetime
from ...plugin import Plugin


class StatsPlugin(Plugin):
    def process_html(self, markup):
        config = markup.document.config
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("#livemark-left").append(
            self.read_asset(
                "markup.html",
                data={"current": datetime.datetime.now(), "format": config.stats.format},
            )
        )
