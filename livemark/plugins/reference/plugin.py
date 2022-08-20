import yaml
from .reference import Reference
from ...plugin import Plugin
from ... import errors


# NOTE:
# We need to render long_description markdown
# We'd like to be able to process it even for a markdown target (as scripts)
# To achieve it we need to update the protocol that HtmlRenderer uses for snippets


class ReferencePlugin(Plugin):
    identity = "reference"
    priority = 60

    # Process

    def process_snippet(self, snippet):
        if snippet.type == "reference" and snippet.lang == "yaml":
            spec = yaml.safe_load(str(snippet.input).strip())
            reference = Reference.from_name(spec["name"])
            if not reference:
                raise errors.Error(f"No object found: {spec}")
            context = {}
            context["class"] = reference
            snippet.output = self.read_asset("markup.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
