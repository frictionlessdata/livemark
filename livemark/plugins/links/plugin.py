from copy import deepcopy
from ...plugin import Plugin


class LinksPlugin(Plugin):
    priority = 10
    profile = {
        "type": "object",
        "properties": {
            "list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"},
                        "hook": {"type": "string"},
                    },
                },
            },
        },
    }

    # Context

    @Plugin.property
    def items(self):
        github = self.document.get_plugin("github")
        items = deepcopy(self.config["list"])
        if github.base_url:
            items.append({"name": "Report", "path": github.report_url})
            items.append({"name": "Fork", "path": github.fork_url})
            items.append({"name": "Edit", "path": github.edit_url})
        return items

    # Process

    def process_config(self, config):
        self.config.setdefault("list", self.config.pop("self", []))

    def process_markup(self, markup):
        if self.config:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-right",
                items=self.items,
            )
