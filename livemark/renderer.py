import bs4
import marko
from marko.ext.gfm import GFM
from marko.html_renderer import HTMLRenderer


class LivemarkRendererMixin(HTMLRenderer):

    # Render

    def render_html_block(self, element):
        markdown = marko.Markdown()
        markdown.use(GFM)
        markdown.use(LivemarkExtension)
        html = bs4.BeautifulSoup(element.children, features="html.parser")
        for node in html.select("*"):
            if len(node.contents) == 1:
                text = node.contents[0]
                if isinstance(text, bs4.element.NavigableString):
                    text = markdown.convert(text)
                    inner = bs4.BeautifulSoup(text, features="html.parser")
                    node.string.replace_with(inner)
        return str(html)


class LivemarkExtension:
    renderer_mixins = [LivemarkRendererMixin]
