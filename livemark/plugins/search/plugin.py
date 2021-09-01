from ...plugin import Plugin


# NOTE:
# It's an initial implementation of the search plugin. Later can be improved:
# - pages concept; it might be preloaded somewhere like Project
# - caching; we don't want to read every doc for every doc
# - use tojson to provide items to the script


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
            item["name"] = document.get_plugin("html").name
            item["path"] = document.path
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
