from ...plugin import Plugin
from ... import errors


class TopicsPlugin(Plugin):
    identity = "topics"
    priority = 20
    validity = {
        "type": "object",
        "properties": {
            "selector": {"type": "string"},
        },
    }

    # Context

    @property
    def selector(self):
        selector = self.config.get("selector", "h2, h3")
        if len(selector.split(",")) > 2:
            raise errors.Error("Maximum topic levels is 2")
        return selector

    # Process

    def process_markup(self, markup):
        if self.document.path != "index":
            markup.add_style("style.css")
            markup.add_script("https://unpkg.com/tocbot@4.12.3/dist/tocbot.min.js")
            markup.add_script("script.js")
            markup.add_markup("markup.html", target="#livemark-right")
