from ...plugin import Plugin
from ... import helpers


class SearchPlugin(Plugin):
    identity = "search"

    # Context

    @property
    def items(self):
        items = []
        documents = [self.document]
        if self.document.project:
            documents = self.document.project.documents
        for document in documents:
            item = {}
            item["name"] = document.get_plugin("site").name
            item["path"] = document.path
            item["relpath"] = helpers.get_url_relpath(document.path, self.document.path)
            item["text"] = document.content
            items.append(item)
        return items

    # Process

    def process_markup(self, markup):
        if self.items:
            url = "https://unpkg.com"
            markup.add_style("style.css")
            markup.add_script(f"{url}/lunr@2.3.9/lunr.min.js")
            markup.add_script(f"{url}/jquery-highlight@3.5.0/jquery.highlight.js")
            markup.add_script(f"{url}/jquery.scrollto@2.1.3/jquery.scrollTo.js")
            markup.add_script("script.js")
            markup.add_markup("markup.html", target="body")
