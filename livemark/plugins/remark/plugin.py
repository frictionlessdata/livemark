import yaml
import marko
from pyquery import PyQuery
from marko.ext.gfm import GFM
from ...plugin import Plugin


class RemarkPlugin(Plugin):
    identity = "remark"

    # Process

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "remark":
                if snippet.lang == "yaml":
                    context = yaml.safe_load(str(snippet.input).strip())
                    snippet.output = self.read_asset("markup.html", **context)
                elif snippet.lang in ["markdown", "html"]:
                    type = snippet.props.get("type", "warning")
                    text = snippet.input
                    if snippet.lang == "markdown":
                        markdown = marko.Markdown()
                        markdown.use(GFM)
                        text = PyQuery(markdown.convert(snippet.input)).html()
                    context = dict(type=type, text=text)
                    snippet.output = self.read_asset("markup.html", **context)

    def process_markup(self, markup):
        markup.add_style("style.css")
