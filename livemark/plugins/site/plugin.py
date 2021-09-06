from ...plugin import Plugin
from ...markup import Markup


# TODO:
# Handle possible double quotes in title/description/keywords


class SitePlugin(Plugin):
    identity = "site"
    validity = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "keywords": {"type": "string"},
            "basepath": {"type": "string"},
            "favicon": {"type": "string"},
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

    @property
    def basepath(self):
        return self.config.get("basepath")

    @property
    def favicon(self):
        return self.config.get("favicon")

    # Process

    def process_document(self, document):
        if document.format == "html":
            markup = Markup(self.read_asset("markup.html", plugin=self))
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
                markup.add_markup(document.output, target="#livemark-main")
            markup.process(document)
            document.output = "<!doctype html>\n" + markup.output
