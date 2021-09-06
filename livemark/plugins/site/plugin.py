from ...plugin import Plugin


class SitePlugin(Plugin):
    identity = "site"
    validity = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "keywords": {"type": "string"},
            "basepath": {"type": "string"},
            "favicon": {"type": "string"},
        },
    }

    # Context

    @property
    def name(self):
        return self.config.get("name", self.document.name)

    @property
    def title(self):
        return self.config.get("title", self.document.title)

    @property
    def description(self):
        return self.config.get("description", self.document.description)

    @property
    def keywords(self):
        return self.config.get("keywords", self.document.keywords)

    @property
    def basepath(self):
        return self.config.get("basepath")

    @property
    def favicon(self):
        return self.config.get("favicon")

    # Process

    def process_markup(self, markup):
        pass
