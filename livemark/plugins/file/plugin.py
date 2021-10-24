from ...plugin import Plugin
from ... import helpers


# NOTE:
# We'd like to be able to process it even for a markdown target (as scripts)
# To achieve it we need to update the protocol that HtmlRenderer uses for snippets


class FilePlugin(Plugin):
    identity = "file"

    # Process

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "file":
                lang = snippet.lang
                text = helpers.read_file(snippet.input.strip()).strip()
                snippet.output = self.read_asset("markup.html", lang=lang, text=text)
