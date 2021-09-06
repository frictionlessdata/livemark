from ...plugin import Plugin


class AboutPlugin(Plugin):
    identity = "about"
    priority = 20
    validity = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
        },
    }

    # Context

    @property
    def text(self):
        site = self.document.get_plugin("site")
        text = self.config.get("text")
        if not text:
            if site.description:
                text = site.description.split(". ")[0]
        return text

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup("markup.html", target="#livemark-right")
