import marko
import pyquery
import frictionless
from marko.ext.gfm import GFM
from jinja2 import Environment, FileSystemLoader
from .renderer import HtmlExtension
from ...plugin import Plugin
from ...system import system


class HtmlPlugin(Plugin):
    def process_document(self, document):
        if document.format == "html":

            # Preprocess document
            # TODO: move to the "logic" plugin?
            templating = Environment(loader=FileSystemLoader("."), trim_blocks=True)
            template = templating.from_string(document.input)
            output = template.render(frictionless=frictionless)

            # Convert document
            markdown = marko.Markdown()
            markdown.use(GFM)
            markdown.use(HtmlExtension)
            output = markdown.convert(output).strip()

            # Create html
            html = pyquery(self.read_asset("markup.html"))
            html("head").append(self.read_asset("style.css", tag="style"))
            html("body").append(self.read_asset("script.js", tag="script"))
            html("#livemark-main").append(output)

            # Process/save html
            system.process_html(html)
            document.output = html.html()
