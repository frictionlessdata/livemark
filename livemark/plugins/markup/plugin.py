import marko
from pyquery import PyQuery
from marko.ext.gfm import GFM
from ..html.renderer import HtmlExtension
from ...plugin import Plugin


class MarkupPlugin(Plugin):
    def process_snippet(self, snippet):
        if snippet.format == "html":
            if "markup" in snippet.header:
                if "html" in snippet.header:
                    markdown = marko.Markdown()
                    markdown.use(GFM)
                    markdown.use(HtmlExtension)
                    query = PyQuery(snippet.input)
                    for node in query.find(".markdown"):
                        node = PyQuery(node)
                        if not node.children():
                            html = markdown.convert(node.text())
                            node.html(html)
                    snippet.output = query.outer_html() + "\n"

    def process_markup(self, markup):
        markup.add_style("https://unpkg.com/bootstrap@4.6.0/dist/css/bootstrap.min.css")
