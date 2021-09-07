import yaml
from ...plugin import Plugin


class VideoPlugin(Plugin):
    identity = "video"
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
            if snippet.type.startswith("video") and snippet.lang == "yaml":
                context = yaml.safe_load(str(snippet.input).strip())
                context.setdefault("width", self.width)
                context.setdefault("height", self.height)
                if snippet.type == "video":
                    snippet.output = self.read_asset("base.html", **context)
                elif snippet.type == "video/youtube":
                    snippet.output = self.read_asset("youtube.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
