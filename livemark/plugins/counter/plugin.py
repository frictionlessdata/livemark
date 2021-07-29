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

    def process_markup(self, markup):
        if not self.config:
            return

        # Prepare context
        type = self.config.get("type")
        code = self.config.get("code")

        # Update markup
        if type == "google":
            markup.add_markup(
                "markup.html",
                target="head",
                code=code,
            )
