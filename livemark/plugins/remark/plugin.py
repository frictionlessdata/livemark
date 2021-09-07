import yaml
from ...plugin import Plugin


# NOTE:
# We might need to rebase on Docusarus-like styling/features for remarks?


class RemarkPlugin(Plugin):
    identity = "remark"

    # Process

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "remark" and snippet.lang == "yaml":
                context = yaml.safe_load(str(snippet.input).strip())
                snippet.output = self.read_asset("markup.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
