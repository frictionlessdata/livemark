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
            if snippet.type == "video":
                if snippet.lang == "yaml":
                    spec_yaml = str(snippet.input).strip()
                    spec_python = yaml.safe_load(spec_yaml)
                    type = spec_python.get("type")
                    code = spec_python.get("code")
                    if type == "youtube" and code:
                        width = spec_python.get("width", self.width)
                        height = spec_python.get("height", self.height)
                        snippet.output = self.read_asset(
                            "markup.html",
                            code=code,
                            width=width,
                            height=height,
                        )

    def process_markup(self, markup):
        markup.add_style("style.css")
