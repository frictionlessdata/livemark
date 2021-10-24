import marko
from .renderer import MarkdownRenderer
from ...plugin import Plugin


class MarkdownPlugin(Plugin):
    identity = "markdown"
    priority = 20

    # Process

    def process_document(self, document):
        if document.format == "md":
            markdown = marko.Markdown(renderer=MarkdownRenderer)
            output = markdown.parse(document.content)
            markdown.renderer.document = document
            output = markdown.render(output)
            if document.preface:
                output = document.preface.join(["---"] * 2) + "\n\n" + output
            document.output = output
