import datetime
from ...plugin import Plugin


class StatsPlugin(Plugin):
    priority = 60

    def process_markup(self, markup):
        code = markup.plugin_config["analytics"]["code"]
        markup.add_style("style.css")
        # TODO: move to the head and make async?
        markup.add_script(f"https://www.googletagmanager.com/gtag/js?id={code}")
        markup.add_script("script.js", config=markup.plugin_config)
        markup.add_markup(
            "markup.html",
            action="prepend",
            target="#livemark-main",
            config=markup.plugin_config,
            current=datetime.datetime.now(),
        )
