import marko
from .renderer import MarkdownRenderer
from ...plugin import Plugin


class MarkdownPlugin(Plugin):
    def process_document(self, document):
        if document.format == "md":
            markdown = marko.Markdown(renderer=MarkdownRenderer)
            output = markdown.parse(document.input)
            markdown.renderer.document = document
            output = markdown.render(output)
            if document.preface:
                output = document.preface.join(["---"] * 2) + "\n" + output
            document.output = output
