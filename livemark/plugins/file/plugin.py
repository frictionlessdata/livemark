from ...plugin import Plugin
from ... import helpers


# NOTE:
# Support injecting into markdown (not only for html using markup) (see ReferencePlugin)


class FilePlugin(Plugin):
    identity = "file"

    # Process

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "file":
                lang = snippet.lang
                text = helpers.read_file(snippet.input.strip()).strip()
                snippet.output = self.read_asset("markup.html", lang=lang, text=text)
