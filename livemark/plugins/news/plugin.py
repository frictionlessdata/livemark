import hashlib
from ...plugin import Plugin


class NewsPlugin(Plugin):
    identity = "news"
    validity = {
        "type": "object",
        "required": ["text"],
        "properties": {
            "text": {"type": "string"},
        },
    }

    # Context

    @property
    def text(self):
        return self.config.get("text")

    @property
    def code(self):
        hash = hashlib.md5()
        hash.update(self.text.encode("utf-8"))
        code = hash.hexdigest()
        return code

    # Process

    def process_markup(self, markup):
        if self.text:
            markup.add_style("style.css")
            markup.add_markup("markup.html")
