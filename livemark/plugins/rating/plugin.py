from ...plugin import Plugin


class RatingPlugin(Plugin):
    priority = 40
    profile = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
        },
    }

    @Plugin.property
    def type(self):
        return self.config.get("type", "star")

    @Plugin.property
    def user(self):
        github = self.get_plugin("github")
        return github.user

    @Plugin.property
    def repo(self):
        github = self.get_plugin("github")
        return github.repo

    # Process

    def process_markup(self, markup):
        if not self.config or not self.user or not self.repo:
            return

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            user=self.user,
            repo=self.repo,
            type=self.type,
        )
