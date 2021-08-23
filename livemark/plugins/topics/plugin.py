from ...plugin import Plugin


# TODO: limit selector levels?
# TODO: support two-level menu items?
class TopicsPlugin(Plugin):
    name = "topics"
    priority = 60
    profile = {
        "type": "object",
        "properties": {
            "selector": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def selector(self):
        return self.config.get("selector", "h2, h3")

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/tocbot@4.12.3/dist/tocbot.min.js")
        markup.add_script("script.js")
        markup.add_markup("markup.html", target="#livemark-left")
