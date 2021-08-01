import marko
from .renderer import MarkdownRenderer
from ...plugin import Plugin


class MarkdownPlugin(Plugin):
    def process_document(self, document):
        if document.format != "md":
            return

        # Update document
        markdown = marko.Markdown(renderer=MarkdownRenderer)
        output = markdown.parse(document.content)
        markdown.renderer.document = document
        output = markdown.render(output)
        if document.preface:
            output = document.preface.join(["---"] * 2) + "\n\n" + output
        document.output = output
