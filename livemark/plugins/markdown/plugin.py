import marko
from .renderer import MarkdownRenderer
from ..plugin import Plugin


class MarkdownPlugin(Plugin):
    def process_document(self, document):
        if document.format in ["md"]:
            markdown = marko.Markdown(renderer=MarkdownRenderer)
            # TODO: handle frontmatter
            document.output = markdown.convert(document.input)
