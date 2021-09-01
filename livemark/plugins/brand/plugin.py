from ...plugin import Plugin


class BrandPlugin(Plugin):
    identity = "brand"
    priority = 80
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
        return self.config.get("text", html.title)

    @property
    def title_extra(self):
        html = self.document.get_plugin("html")
        if self.text != html.title:
            return f" | {self.text}"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup("markup.html", target="#livemark-left")
        if self.title_extra:
            markup.query("title").append(self.title_extra)
