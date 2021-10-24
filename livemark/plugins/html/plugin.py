import marko
from marko.ext.gfm import GFM
from .renderer import HtmlExtension
from ...plugin import Plugin


class HtmlPlugin(Plugin):
    identity = "html"
    priority = 20

    # Process

    def process_document(self, document):
        if document.format == "html":
            markdown = marko.Markdown()
            markdown.use(GFM)
            markdown.use(HtmlExtension)
            output = markdown.parse(document.content)
            markdown.renderer.document = document
            output = markdown.render(output)
            output = output.strip()
            document.output = output
