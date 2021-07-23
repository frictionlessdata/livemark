import marko
from marko.ext.gfm import GFM
from .renderer import HtmlExtension
from ...markup import Markup
from ...plugin import Plugin


class HtmlPlugin(Plugin):
    def process_document(self, document):
        if document.format == "html":

            # Process content
            markdown = marko.Markdown()
            markdown.use(GFM)
            markdown.use(HtmlExtension)
            output = markdown.convert(document.input).strip()

            # Process markup
            markup = Markup(self.read_asset("markup.html"), document=document)
            markup.query("head").append(self.read_asset("style.css", tag="style"))
            markup.query("body").append(self.read_asset("script.js", tag="script"))
            markup.query("#livemark-main").append(output)
            markup.process()
            document.output = markup.output
