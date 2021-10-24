import yaml
from docstring_parser import parse
from ...plugin import Plugin
from ... import helpers
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
            object = helpers.load_object(spec.get("path"))
            if not object:
                raise errors.Error(f"No object found: {spec}")
            context = {}
            context["name"] = object.__name__
            context["info"] = parse(object.__doc__)
            snippet.output = self.read_asset("markup.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
