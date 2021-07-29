from ...plugin import Plugin


class LinksPlugin(Plugin):
    priority = 20
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

    def process_markup(self, markup):
        github = self.get_plugin("github")
        if not self.config:
            return

        # Prepare context
        list = self.config.get("list", []).copy()
        if github.config:
            list.append({"name": "Report", "path": github.config["report_url"]})
        list.append({"name": "Print", "hook": "window.print();return false;"})
        if github.config:
            list.append({"name": "Edit", "path": github.config["edit_url"]})

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            list=list,
        )
