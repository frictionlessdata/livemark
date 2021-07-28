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
        if not markup.plugin_config:
            return

        # Prepare context
        github = markup.document.config.get("github", {})
        list = markup.plugin_config.get("list", []).copy()
        if github:
            list.append({"name": "Report", "path": github["report_url"]})
        list.append({"name": "Print", "hook": "window.print();return false;"})
        if github:
            list.append({"name": "Edit", "path": github["edit_url"]})

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            list=list,
        )
