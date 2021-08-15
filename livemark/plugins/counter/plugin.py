from ...plugin import Plugin


class CounterPlugin(Plugin):
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
    def type(self):
        return self.config.get("type")

    @Plugin.property
    def code(self):
        return self.config.get("code")

    # Process

    def process_markup(self, markup):
        if self.config and self.type == "google":
            markup.add_markup(
                "markup.html",
                target="head",
                code=self.code,
            )
