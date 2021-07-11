import io
import sys
import subprocess
import contextlib
from copy import copy
from marko.inline import RawText
from marko.block import FencedCode
from marko.md_renderer import MarkdownRenderer


class LivemarkMarkdownRenderer(MarkdownRenderer):

    # Render

    def render_quote(self, element):
        return super().render_quote(element).rstrip() + "\n"

    def render_fenced_code(self, element):
        header = [element.lang] + element.extra.split()
        if "script" in header:
            code = self.render_children(element).strip()
            source = element

            # Execute code
            output = None
            if "python" in header:
                with capture() as stdout:
                    exec(code, globals())
                output = stdout.getvalue().strip()
            elif "bash" in header:
                try:
                    output = subprocess.check_output(code, shell=True).decode().strip()
                except Exception as exception:
                    output = exception.output.decode().strip()
            output = "\n".join(line.rstrip() for line in output.splitlines())

            # Write code
            if output is not None:

                # Locate target
                target = None
                index = self.root_node.children.index(source)
                if len(self.root_node.children) > index + 1:
                    item = self.root_node.children[index + 1]
                    if isinstance(item, FencedCode):
                        target = item

                # Create target
                if output and not target:
                    target = copy(source)
                    target.lang = ""
                    target.extra = ""
                    self.root_node.children.insert(index + 1, target)

                # Update target
                if target:
                    target.children = [RawText(output)]

        return super().render_fenced_code(element)


# Internal


@contextlib.contextmanager
def capture(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
