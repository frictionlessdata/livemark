from ...plugin import Plugin


class RatingPlugin(Plugin):
    priority = 40
    profile = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
        },
    }

    def process_markup(self, markup):
        github = self.get_plugin("github")
        if not self.config or not github.config:
            return

        # Prepare context
        type = self.config.get("type", "star")
        user = github.config["user"]
        repo = github.config["repo"]

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            user=user,
            repo=repo,
            type=type,
        )
