import yaml
from ...plugin import Plugin


class ImagePlugin(Plugin):
    identity = "image"
    validity = {
        "type": "object",
        "properties": {
            "width": {"type": "number"},
            "height": {"type": "number"},
        },
    }

    # Context

    @property
    def width(self):
        return self.config.get("width", 600)

    @property
    def height(self):
        return self.config.get("height", 400)

    # Process

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "image":
                if snippet.lang == "yaml":
                    context = yaml.safe_load(str(snippet.input).strip())
                    context.setdefault("width", self.width)
                    context.setdefault("height", self.height)
                    if context["type"] == "native":
                        snippet.output = self.read_asset("native.html", **context)
                    elif context["type"] == "instagram":
                        snippet.output = self.read_asset("instagram.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
