from ...plugin import Plugin


class BlogPlugin(Plugin):
    name = "blog"
    profile = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
        },
    }

    # Context

    @Plugin.property
    def items(self):
        return []

    # Process

    def process_markup(self, markup):
        pass
