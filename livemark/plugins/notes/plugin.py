import os
from datetime import datetime
from ...plugin import Plugin


class NotesPlugin(Plugin):
    identity = "notes"
    priority = 50
    validity = {
        "type": "object",
        "properties": {
            "format": {"type": "string"},
        },
    }

    # Context

    @property
    def format(self):
        return self.config.get("format", "%Y-%m-%d %H:%M")

    @property
    def current(self):
        return datetime.fromtimestamp(os.path.getmtime(self.document.source))

    @property
    def edit_url(self):
        github = self.document.get_plugin("github")
        if github:
            return github.edit_url

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup("markup.html", target="#livemark-main", action="prepend")
