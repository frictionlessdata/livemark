from ...plugin import Plugin


class LinksPlugin(Plugin):
    priority = 20

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare context
        # TODO: remove this condition when it's normalized
        config = markup.plugin_config if isinstance(markup.plugin_config, dict) else {}
        github = markup.document.config.get("github", {})
        list = config.get("list", []).copy()
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
