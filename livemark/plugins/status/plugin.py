from ...plugin import Plugin


class StatusPlugin(Plugin):
    priority = 40

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare context
        github = markup.document.config.get("github")
        type = markup.plugin_config.get("type", "star")

        # Update markup
        if github:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-right",
                github=github,
                type=type,
            )
