from ...plugin import Plugin


class CounterPlugin(Plugin):
    identity = "counter"
    validity = {
        "type": "object",
        "required": ["type", "code"],
        "properties": {
            "type": {"type": "string"},
            "code": {"type": "string"},
        },
    }

    # Context

    @property
    def type(self):
        return self.config.get("type")

    @property
    def code(self):
        return self.config.get("code")

    # Process

    def process_markup(self, markup):
        if self.type == "google":
            markup.add_markup("google.html", target="head")
        elif self.type == "plausible":
            markup.add_markup("plausible.html", target="head")
