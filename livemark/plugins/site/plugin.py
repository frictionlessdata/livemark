from ...plugin import Plugin


class SitePlugin(Plugin):
    identity = "site"
    priority = 20
    validity = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
        },
    }

    # Process

    def process_markup(self, markup):
        pass
