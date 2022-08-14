from copy import deepcopy
from ...plugin import Plugin


class LinksPlugin(Plugin):
    identity = "links"
    priority = 10
    validity = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
                    },
                },
            },
        },
    }

    # Context

    @property
    def items(self):
        github = self.document.get_plugin("github")
        items = deepcopy(self.config.get("items", []))
        if github:
            if github.report_url:
                items.append({"name": "Report", "path": github.report_url})
            if github.fork_url:
                items.append({"name": "Fork", "path": github.fork_url})
        return items

    # Process

    def process_markup(self, markup):
        if self.document.path == "index":
            if self.items:
                markup.add_style("style.css")
                markup.add_markup("markup.html", target="#livemark-right")
