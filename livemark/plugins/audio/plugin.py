import yaml
from ...plugin import Plugin


class AudioPlugin(Plugin):
    identity = "audio"
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
            if snippet.type.startswith("audio") and snippet.lang == "yaml":
                context = yaml.safe_load(str(snippet.input).strip())
                context.setdefault("width", self.width)
                context.setdefault("height", self.height)
                if snippet.type == "audio":
                    snippet.output = self.read_asset("base.html", **context)
                elif snippet.type == "audio/soundcloud":
                    snippet.output = self.read_asset("soundcloud.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
