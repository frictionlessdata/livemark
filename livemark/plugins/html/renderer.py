from copy import copy
from marko import html_renderer
from marko.inline import RawText
from marko.block import FencedCode
from ...snippet import Snippet


# NOTE:
# Move all the `script/task` related code to corresponding plugins


class HtmlRenderer(html_renderer.HTMLRenderer):

    # Render

    def render_fenced_code(self, element):
        input = element.children[0].children
        header = [element.lang] + element.extra.split()
        snippet = Snippet(input, header=header)
        snippet.process(self.document)

        # Script
        if snippet.output is not None:
            if snippet.type == "script":

                # Remove target
                index = self.root_node.children.index(element)
                if len(self.root_node.children) > index + 1:
                    item = self.root_node.children[index + 1]
                    if isinstance(item, FencedCode):
                        del self.root_node.children[index + 1]

                # Return output
                output = super().render_fenced_code(element)
                target = copy(element)
                target.lang = "markup"
                target.extra = ""
                target.children = [RawText(snippet.output)]
                output += "\n"
                output += super().render_fenced_code(target)
                return output

            return snippet.output

        # Task
        if snippet.type == "task" and snippet.props.get("id"):

            # Return output
            task = snippet.props["id"]
            target = copy(element)
            target.lang = "bash"
            target.extra = ""
            target.children = [RawText(f"$ livemark run {task}")]
            output = '<div class="livemark-task">'
            output += super().render_fenced_code(target)
            output += "\n"
            output += super().render_fenced_code(element)
            output += "</div>"
            return output

        return super().render_fenced_code(element)


class HtmlExtension:
    renderer_mixins = [HtmlRenderer]
