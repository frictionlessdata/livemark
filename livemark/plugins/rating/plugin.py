from ...plugin import Plugin


class RatingPlugin(Plugin):
    identity = "rating"
    priority = 30
    validity = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
        },
    }

    # Context

    @property
    def type(self):
        return self.config.get("type", "star")

    @property
    def user(self):
        github = self.document.get_plugin("github")
        if github:
            return github.user

    @property
    def repo(self):
        github = self.document.get_plugin("github")
        if github:
            return github.repo

    # Process

    def process_markup(self, markup):
        if self.user and self.repo:
            markup.add_style("style.css")
            markup.add_markup("markup.html", target="#livemark-right")
