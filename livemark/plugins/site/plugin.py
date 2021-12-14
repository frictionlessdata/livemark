import os
from ...plugin import Plugin
from ...markup import Markup
from ... import helpers


# NOTE:
# It will be great to have a "Show the source" button for every heading


class SitePlugin(Plugin):
    identity = "site"
    validity = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "keywords": {"type": "string"},
            "favicon": {"type": "string"},
            "layout": {"type": "string"},
            "styles": {"type": "array"},
            "scripts": {"type": "array"},
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
    def favicon(self):
        if self.config.get("favicon"):
            return helpers.get_relpath(self.config.get("favicon"), self.document.path)

    @property
    def layout(self):
        layout = self.config.get("layout")
        return os.path.abspath(layout) if layout else "markup.html"

    @property
    def styles(self):
        styles = []
        for path in self.config.get("styles", []):
            path = path if helpers.is_remote_path(path) else os.path.abspath(path)
            styles.append(path)
        return styles

    @property
    def scripts(self):
        scripts = []
        for path in self.config.get("scripts", []):
            path = path if helpers.is_remote_path(path) else os.path.abspath(path)
            scripts.append(path)
        return scripts

    # Process

    def process_document(self, document):
        if document.format == "html":
            markup = Markup(self.read_asset(self.layout))
            with markup.bind(self):
                bs_url = "https://unpkg.com/bootstrap@4.6.0"
                fa_url = "https://unpkg.com/@fortawesome/fontawesome-free@5.15.4"
                pm_url = "https://unpkg.com/prismjs@1.23.0"
                jq_url = "https://unpkg.com/jquery@3.6.0"
                pp_url = "https://unpkg.com/popper.js@1.16.1"
                ld_url = "https://unpkg.com/lodash@4.17.21"
                markup.add_style(f"{fa_url}/css/all.min.css")
                markup.add_style(f"{bs_url}/dist/css/bootstrap.min.css")
                markup.add_style(f"{pm_url}/themes/prism.css")
                markup.add_style("style.css")
                for path in self.styles:
                    markup.add_style(path)
                markup.add_script(f"{ld_url}/lodash.min.js")
                markup.add_script(f"{jq_url}/dist/jquery.min.js")
                markup.add_script(f"{pp_url}/dist/umd/popper.min.js")
                markup.add_script(f"{bs_url}/dist/js/bootstrap.min.js")
                markup.add_script(f"{pm_url}/components/prism-core.min.js")
                markup.add_script(f"{pm_url}/plugins/autoloader/prism-autoloader.min.js")
                markup.add_script("script.js")
                for path in self.scripts:
                    markup.add_script(path)
                markup.add_markup(document.output, target="#livemark-main")
            markup.process(document)
            document.output = "<!doctype html>\n" + markup.output
