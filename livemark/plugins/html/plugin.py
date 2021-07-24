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
            input = self.read_asset("markup.html")
            markup = Markup(input, document=document)
            with markup.bind(self):
                markup.add_style("style.css")
                markup.add_script("script.js")
                markup.add_markup(output, target="#livemark-main")
            markup.process()

            # Update document
            document.output = markup.output
