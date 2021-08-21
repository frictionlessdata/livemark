from ...plugin import Plugin


class RatingPlugin(Plugin):
    priority = 30
    profile = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def type(self):
        return self.config.get("type", "star")

    @Plugin.property
    def user(self):
        github = self.document.get_plugin("github")
        return github.user

    @Plugin.property
    def repo(self):
        github = self.document.get_plugin("github")
        return github.repo

    # Process

    def process_markup(self, markup):
        if self.config and self.user and self.repo:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-right",
                user=self.user,
                repo=self.repo,
                type=self.type,
            )
