from ...plugin import Plugin


class LinksPlugin(Plugin):
    priority = 20
    profile = {
        "type": "object",
        "properties": {
            "items": {
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

    def process_config(self, config):
        self.config.setdefault("items", self.config.pop("self", []))

    def process_markup(self, markup):
        github = self.get_plugin("github")
        if not self.config:
            return

        # Prepare context
        items = self.config["items"].copy()
        if github.config:
            items.append({"name": "Report", "path": github.config["report_url"]})
        items.append({"name": "Print", "hook": "window.print();return false;"})
        if github.config:
            items.append({"name": "Fork", "path": github.config["fork_url"]})
            items.append({"name": "Edit", "path": github.config["edit_url"]})

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            items=items,
        )
