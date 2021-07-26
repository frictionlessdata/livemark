from ...plugin import Plugin


class LinksPlugin(Plugin):
    priority = 20

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare list
        # TODO: improve this code
        # TODO: rename list to something else
        github = markup.document.config.get("github", {})
        config = markup.plugin_config if isinstance(markup.plugin_config, dict) else {}
        list = config.get("list", []).copy()
        if github:
            list.append(
                {
                    "name": "Report",
                    "path": f"https://github.com/{github['user']}/{github['repo']}/issues",
                }
            )
        list.append(
            {
                "name": "Print",
                "path": "#",
                "hook": "window.print();return false;",
            }
        )
        if github:
            list.append(
                {
                    "name": "Edit",
                    "path": f"https://github.com/{github['user']}/{github['repo']}/edit/main/{markup.document.source}",
                }
            )

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            list=list,
        )
