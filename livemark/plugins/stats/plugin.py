import os
from datetime import datetime
from ...plugin import Plugin


class StatsPlugin(Plugin):
    priority = 60

    # TODO: move gtag to the head and make async?
    def process_markup(self, markup):

        # Prepare code/current
        code = markup.plugin_config["analytics"]["code"]
        current = datetime.fromtimestamp(os.path.getmtime(markup.document.source))

        # Update markup
        markup.add_style("style.css")
        markup.add_script(f"https://www.googletagmanager.com/gtag/js?id={code}")
        markup.add_script("script.js", config=markup.plugin_config)
        markup.add_markup(
            "markup.html",
            action="prepend",
            target="#livemark-main",
            config=markup.plugin_config,
            current=current,
        )
