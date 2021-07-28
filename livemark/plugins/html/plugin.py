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
            output = markdown.parse(document.input)
            markdown.renderer.document = document
            output = markdown.render(output)
            output = output.strip()

            # Prepare context
            title = document.plugin_config.get("title", document.title)
            description = document.plugin_config.get("description", document.description)
            keywords = document.plugin_config.get("keywords", document.keywords)

            # Process markup
            # TODO: infer description/keywords
            input = self.read_asset(
                "markup.html",
                title=title,
                description=description,
                keywords=keywords,
            )
            markup = Markup(input, document=document)
            with markup.bind(self):
                markup.add_style("https://unpkg.com/prismjs@1.23.0/themes/prism.css")
                markup.add_style("style.css")
                markup.add_script(
                    "https://unpkg.com/prismjs@1.23.0/components/prism-core.min.js"
                )
                markup.add_script(
                    "https://unpkg.com/prismjs@1.23.0/plugins/autoloader/prism-autoloader.min.js"
                )
                markup.add_script("script.js")
                markup.add_markup(output, target="#livemark-main")
            markup.process()

            # Update document
            document.output = markup.output
