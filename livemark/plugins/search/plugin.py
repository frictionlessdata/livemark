from pathlib import Path
from ...document import Document
from ...plugin import Plugin


# NOTE:
# It's an initial implementation of the search plugin. Later can be improved:
# - pages concept; it might be preloaded somewhere like Project
# - caching; we don't want to read every doc for every doc


class SearchPlugin(Plugin):

    # Context

    @Plugin.property
    def items(self):
        pages = self.document.get_plugin("pages")

        # Single page
        items = [
            {
                "name": self.document.title,
                "path": self.document.path,
                "text": self.document.content,
            }
        ]

        # Multiple pages
        if pages:
            items = []
            for item in pages.flatten_items:
                path = str(Path(item["path"] or "index").with_suffix(".md"))
                document = Document(path)
                document.read()
                items.append(
                    {
                        "name": item["name"],
                        "path": item["path"],
                        "text": document.content,
                    }
                )

        return items

    # Process

    def process_markup(self, markup):
        if self.items:
            url = "https://unpkg.com"
            markup.add_style("style.css")
            markup.add_script(f"{url}/lunr@2.3.9/lunr.min.js")
            markup.add_script(f"{url}/jquery-highlight@3.5.0/jquery.highlight.js")
            markup.add_script(f"{url}/jquery.scrollto@2.1.3/jquery.scrollTo.js")
            markup.add_script("script.js", items=self.items)
            markup.add_markup(
                "markup.html",
                target="body",
            )
