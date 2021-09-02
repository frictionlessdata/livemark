from ...plugin import Plugin


# TODO: use base url from the SitePlugin


class CommentsPlugin(Plugin):
    identity = "comments"
    priority = 45
    validity = {
        "type": "object",
        "properties": {
            "enable": {"type": "boolean"},
        },
    }

    # Context

    @property
    def code(self):
        return self.config.get("code")

    @property
    def link(self):
        return self.config.get("link")

    # Process

    def process_markup(self, markup):
        if self.code and self.link:
            markup.add_style("style.css")
            markup.add_script("https://livemark.disqus.com/count.js")
            markup.add_script("script.js")
            markup.add_markup("markup.html", target="#livemark-main")
