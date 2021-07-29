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
        config = markup.document.config.get(self.name)
        if not config:
            return

        # Prepare context
        type = config.get("type")
        code = config.get("code")

        # Update markup
        if type == "google":
            markup.add_markup(
                "markup.html",
                target="head",
                code=code,
            )
