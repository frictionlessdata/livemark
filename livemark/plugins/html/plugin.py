import marko
from marko.ext.gfm import GFM
from .renderer import HtmlExtension
from ...markup import Markup
from ...plugin import Plugin


# NOTE:
# Handle possible double quotes in title/description/keywords


class HtmlPlugin(Plugin):
    identity = "html"
    validity = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "keywords": {"type": "string"},
        },
    }

    # Context

    @property
    def name(self):
        return self.config.get("name", self.document.name)

    @property
    def title(self):
        return self.config.get("title", self.document.title)

    @property
    def description(self):
        return self.config.get("description", self.document.description)

    @property
    def keywords(self):
        return self.config.get("keywords", self.document.keywords)

    # Process

    def process_document(self, document):
        if document.format == "html":

            # Process content
            markdown = marko.Markdown()
            markdown.use(GFM)
            markdown.use(HtmlExtension)
            output = markdown.parse(document.content)
            markdown.renderer.document = document
            output = markdown.render(output)
            output = output.strip()

            # Create markup
            markup = Markup(
                self.read_asset(
                    "markup.html",
                    title=self.title,
                    description=self.description,
                    keywords=self.keywords,
                )
            )

            # Process markup
            with markup.bind(self):
                bs_url = "https://unpkg.com/bootstrap@4.6.0"
                fa_url = "https://unpkg.com/@fortawesome/fontawesome-free@5.15.4"
                pm_url = "https://unpkg.com/prismjs@1.23.0"
                jq_url = "https://unpkg.com/jquery@3.6.0"
                pp_url = "https://unpkg.com/popper.js@1.16.1"
                markup.add_style(f"{fa_url}/css/all.min.css")
                markup.add_style(f"{bs_url}/dist/css/bootstrap.min.css")
                markup.add_style(f"{pm_url}/themes/prism.css")
                markup.add_style("style.css")
                markup.add_script(f"{jq_url}/dist/jquery.min.js")
                markup.add_script(f"{pp_url}/dist/umd/popper.min.js")
                markup.add_script(f"{bs_url}/dist/js/bootstrap.min.js")
                markup.add_script(f"{pm_url}/components/prism-core.min.js")
                markup.add_script(f"{pm_url}/plugins/autoloader/prism-autoloader.min.js")
                markup.add_script("script.js")
                markup.add_markup(output, target="#livemark-main")
            markup.process(document)

            # Update document
            document.output = "<!doctype html>\n" + markup.output
