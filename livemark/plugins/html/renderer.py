from copy import copy
from marko import html_renderer
from marko.inline import RawText
from ...snippet import Snippet


class HtmlRenderer(html_renderer.HTMLRenderer):

    # Render

    def render_fenced_code(self, element):
        input = element.children[0].children
        header = [element.lang] + element.extra.split()
        snippet = Snippet(input, header=header)
        snippet.process(self.document)
        if snippet.output is not None:
            if "script" in snippet.header:
                output = super().render_fenced_code(element)
                target = copy(element)
                target.lang = "markup"
                target.extra = ""
                target.children = [RawText(snippet.output)]
                output += "\n"
                output += super().render_fenced_code(target)
                return output
            return snippet.output
        return super().render_fenced_code(element)


class HtmlExtension:
    renderer_mixins = [HtmlRenderer]
