import os
from datetime import datetime
from ...plugin import Plugin


class StatsPlugin(Plugin):
    priority = 60

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare context
        format = markup.plugin_config.get("format", "%Y-%m-%d %H:%M:%S")
        current = datetime.fromtimestamp(os.path.getmtime(markup.document.source))

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            action="prepend",
            target="#livemark-main",
            format=format,
            current=current,
        )
