from marko import html_renderer
from ...snippet import Snippet


class HtmlRenderer(html_renderer.HTMLRenderer):

    # Render

    def render_html_block(self, element):
        snippet = Snippet(element.children, format="html", header=["markup"])
        snippet.process()
        return snippet.output

    def render_fenced_code(self, element):
        input = element.children[0].children
        header = [element.lang] + element.extra.split()
        snippet = Snippet(input, format="html", header=header)
        snippet.process()
        # TODO: fix this logic
        if snippet.output:
            return snippet.output
        return super().render_fenced_code(element)


class HtmlExtension:
    renderer_mixins = [HtmlRenderer]
