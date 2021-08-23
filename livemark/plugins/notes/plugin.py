import os
from datetime import datetime
from ...plugin import Plugin


class NotesPlugin(Plugin):
    name = "notes"
    priority = 50
    profile = {
        "type": "object",
        "properties": {
            "format": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def format(self):
        return self.config.get("format", "%Y-%m-%d %H:%M")

    @Plugin.property
    def current(self):
        return datetime.fromtimestamp(os.path.getmtime(self.document.source))

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup("markup.html", target="#livemark-main", action="prepend")
