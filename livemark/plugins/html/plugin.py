import marko
from marko.ext.gfm import GFM
from .renderer import HtmlExtension
from ...markup import Markup
from ...plugin import Plugin


class HtmlPlugin(Plugin):
    profile = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "keywords": {"type": "string"},
        },
    }

    def process_document(self, document):
        if document.format != "html":
            return

        # Process content
        markdown = marko.Markdown()
        markdown.use(GFM)
        markdown.use(HtmlExtension)
        output = markdown.parse(document.content)
        markdown.renderer.document = document
        output = markdown.render(output)
        output = output.strip()

        # Prepare context
        title = self.config.get("title", document.title)
        description = self.config.get("description", document.description)
        keywords = self.config.get("keywords", document.keywords)

        # Create markup
        markup = Markup(
            self.read_asset(
                "markup.html",
                title=title,
                description=description,
                keywords=keywords,
            )
        )

        # Process markup
        with markup.bind(self):
            bs_url = "https://unpkg.com/bootstrap@4.6.0"
            fa_url = "https://unpkg.com/@fortawesome/fontawesome-free@5.15.4"
            prism_url = "https://unpkg.com/prismjs@1.23.0"
            jquery_url = "https://unpkg.com/jquery@3.6.0"
            popper_url = "https://unpkg.com/popper.js@1.16.1"
            markup.add_style(f"{fa_url}/css/all.min.css")
            markup.add_style(f"{bs_url}/dist/css/bootstrap.min.css")
            markup.add_style(f"{prism_url}/themes/prism.css")
            markup.add_style("style.css")
            markup.add_script(f"{jquery_url}/dist/jquery.min.js")
            markup.add_script(f"{popper_url}/dist/popper.min.js")
            markup.add_script(f"{bs_url}/dist/js/bootstrap.min.js")
            markup.add_script(f"{prism_url}/components/prism-core.min.js")
            markup.add_script(f"{prism_url}/plugins/autoloader/prism-autoloader.min.js")
            markup.add_script("script.js")
            markup.add_markup(output, target="#livemark-main")
        markup.process(document)

        # Update document
        document.output = "<!doctype html>\n" + markup.output
