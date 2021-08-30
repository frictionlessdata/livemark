from ...plugin import Plugin


class CounterPlugin(Plugin):
    code = "counter"
    profile = {
        "type": "object",
        "required": ["type", "mark"],
        "properties": {
            "type": {"type": "string"},
            "mark": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def type(self):
        return self.config.get("type")

    @Plugin.property
    def mark(self):
        return self.config.get("mark")

    # Process

    def process_markup(self, markup):
        if self.type == "google":
            markup.add_markup("markup.html", target="head")
