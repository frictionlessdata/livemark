import bs4
import marko
from marko.ext.gfm import GFM
from ..html.renderer import HtmlExtension
from ...plugin import Plugin


class MarkupPlugin(Plugin):
    def process_snippet(self, snippet):
        if snippet.format == "html":
            if "markup" in snippet.header:
                markdown = marko.Markdown()
                markdown.use(GFM)
                markdown.use(HtmlExtension)
                html = bs4.BeautifulSoup(snippet.input, features="html.parser")
                for node in html.select(".markdown"):
                    if len(node.contents) == 1:
                        text = node.contents[0]
                        if isinstance(text, bs4.element.NavigableString):
                            text = markdown.convert(text)
                            inner = bs4.BeautifulSoup(text, features="html.parser")
                            node.string.replace_with(inner)
                snippet.output = str(html)
