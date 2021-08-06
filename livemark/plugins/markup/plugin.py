import marko
import textwrap
from pyquery import PyQuery
from marko.ext.gfm import GFM
from ..html.renderer import HtmlExtension
from ...plugin import Plugin


class MarkupPlugin(Plugin):
    def process_snippet(self, snippet):
        if self.document.format != "html":
            return

        # Update snippet
        if snippet.type == "markup":
            if snippet.lang == "html":
                markdown = marko.Markdown()
                markdown.use(GFM)
                markdown.use(HtmlExtension)
                query = PyQuery(snippet.input)
                for node in query.find(".markdown"):
                    node = PyQuery(node)
                    if not node.children():
                        input = node.text(squash_space=False)
                        input = textwrap.dedent(input).strip("\n")
                        output = markdown.convert(input)
                        node.html(output)
                snippet.output = query.outer_html() + "\n"

    def process_markup(self, markup):
        markup.add_style("https://unpkg.com/bootstrap@4.6.0/dist/css/bootstrap.min.css")
