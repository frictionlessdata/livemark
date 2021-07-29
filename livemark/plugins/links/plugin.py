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
        config_links = self.get_config(markup)
        config_github = self.get_config(markup, plugin="github")
        if not config_links:
            return

        # Prepare context
        list = config_links.get("list", []).copy()
        if config_github:
            list.append({"name": "Report", "path": config_github["report_url"]})
        list.append({"name": "Print", "hook": "window.print();return false;"})
        if config_github:
            list.append({"name": "Edit", "path": config_github["edit_url"]})

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            list=list,
        )
