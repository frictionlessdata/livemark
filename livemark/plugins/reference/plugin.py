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
            references = []
            for pointer in spec.get("references", []):
                reference = Reference.from_name(pointer)
                references.append(reference)
            if not references:
                raise errors.Error(f"No references found: {spec}")
            context = {}
            context["references"] = references
            context["level"] = spec.get("level", 3)
            snippet.output = self.read_asset("markup.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
