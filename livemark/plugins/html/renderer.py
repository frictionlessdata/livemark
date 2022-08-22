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
        if snippet.type == "script" and snippet.output is not None:

            # Remove target
            if self.document.format == "md":
                index = self.root_node.children.index(element)
                if len(self.root_node.children) > index + 1:
                    item = self.root_node.children[index + 1]
                    if isinstance(item, FencedCode):
                        del self.root_node.children[index + 1]

            # Return output
            output = super().render_fenced_code(element)
            if snippet.output:
                target = copy(element)
                target.lang = snippet.props.get("output", "markup")
                target.extra = ""
                target.children = [RawText(snippet.output)]
                output += "\n"
                output += super().render_fenced_code(target)

        # Task
        elif snippet.type == "task" and snippet.props.get("id"):

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

        # Others
        elif snippet.output is not None:
            output = snippet.output

        # Default
        else:
            output = super().render_fenced_code(element)

        # Container
        items = []
        for name, value in snippet.props.items():
            items.append(f'data-{name}="{value}"')
        output = f"<div {' '.join(items)}>{output}</div>"

        return output


class HtmlExtension:
    renderer_mixins = [HtmlRenderer]
