from ...plugin import Plugin
from ... import helpers


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
    def path(self):
        return helpers.get_relpath(".", self.document.path)

    @property
    def text(self):
        site = self.document.get_plugin("site")
        return self.config.get("text", site.title)

    @property
    def title_extra(self):
        site = self.document.get_plugin("site")
        if self.text != site.title:
            return f" | {self.text}"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup("markup.html", target="#livemark-left")
        if self.title_extra:
            markup.query("title").append(self.title_extra)
