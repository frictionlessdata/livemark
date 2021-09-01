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
        html = self.document.get_plugin("html")
        text = self.config.get("text")
        if not text:
            if html.description:
                text = html.description.split(". ")[0]
        return text

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup("markup.html", target="#livemark-right")
