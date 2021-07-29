from ...plugin import Plugin


class StatusPlugin(Plugin):
    priority = 40
    profile = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
        },
    }

    def process_markup(self, markup):
        config_markup = self.get_config(markup)
        config_github = self.get_config(markup, plugin="github")
        if not config_markup or not config_github:
            return

        # Prepare context
        type = config_markup.get("type", "star")
        user = config_github["user"]
        repo = config_github["repo"]

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            user=user,
            repo=repo,
            type=type,
        )
