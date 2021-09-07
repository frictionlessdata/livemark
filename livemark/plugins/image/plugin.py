import yaml
from ...plugin import Plugin


# NOTE:
# Consider that we can have a system when different components can be moved to
# some target destinations. For example, create an image/audio/video/etc as usual
# and move it to carousel or markup columns/etc. It will fix the nested markup limitation


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
            if snippet.type.startswith("image") and snippet.lang == "yaml":
                context = yaml.safe_load(str(snippet.input).strip())
                context.setdefault("width", self.width)
                context.setdefault("height", self.height)
                if snippet.type == "image":
                    snippet.output = self.read_asset("base.html", **context)
                elif snippet.type == "image/instagram":
                    snippet.output = self.read_asset("instagram.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
