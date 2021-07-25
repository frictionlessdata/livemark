import datetime
from ...plugin import Plugin


class StatsPlugin(Plugin):
    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            action="prepend",
            target="#livemark-main",
            config=markup.plugin_config,
            current=datetime.datetime.now(),
        )
