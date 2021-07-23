from copy import copy
from marko import md_renderer
from marko.inline import RawText
from marko.block import FencedCode
from ...snippet import Snippet


class MarkdownRenderer(md_renderer.MarkdownRenderer):

    # Render

    def render_quote(self, element):
        return super().render_quote(element).rstrip() + "\n"

    def render_fenced_code(self, element):
        input = self.render_children(element).strip()
        header = [element.lang] + element.extra.split()
        snippet = Snippet(input, format="md", header=header)
        snippet.process()
        if snippet.output:

            # Locate target
            target = None
            index = self.root_node.children.index(element)
            if len(self.root_node.children) > index + 1:
                item = self.root_node.children[index + 1]
                if isinstance(item, FencedCode):
                    target = item

            # Create target
            if snippet.output and not target:
                target = copy(element)
                target.lang = ""
                target.extra = ""
                self.root_node.children.insert(index + 1, target)

            # Update target
            if target:
                target.children = [RawText(snippet.output)]

        return super().render_fenced_code(element)
