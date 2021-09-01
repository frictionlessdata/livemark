from ...plugin import Plugin


class CounterPlugin(Plugin):
    code = "counter"
    profile = {
        "type": "object",
        "required": ["type", "code"],
        "properties": {
            "type": {"type": "string"},
            "code": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def counter_type(self):
        return self.config.get("type")

    @Plugin.property
    def counter_code(self):
        return self.config.get("code")

    # Process

    def process_markup(self, markup):
        if self.counter_type == "google":
            markup.add_markup("markup.html", target="head")
