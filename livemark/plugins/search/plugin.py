from pathlib import Path
from ...document import Document
from ...plugin import Plugin


# NOTE:
# It's an initial implementation of the search plugin. Later can be improved:
# - pages concept; it might be preloaded somewhere like Project
# - caching; we don't want to read every doc for every doc


class SearchPlugin(Plugin):
    def process_markup(self, markup):
        pages = self.get_plugin("pages")
        if not self.config:
            return

        # Single page
        items = [
            {
                "name": self.document.title,
                "link": f"/{self.document.target}",
                "text": self.document.content,
            }
        ]

        # Multiple pages
        if pages.config:
            items = []
            for item in pages.config["items"]:
                path = Path(item["path"][1:] or "index.html").with_suffix(".md")
                document = Document(path)
                document.read()
                items.append(
                    {
                        "name": item["name"],
                        "link": item["path"],
                        "text": document.content,
                    }
                )

        # Update markup
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/lunr@2.3.9/lunr.min.js")
        markup.add_script("https://unpkg.com/jquery@3.6.0/dist/jquery.min.js")
        markup.add_script("https://unpkg.com/jquery-highlight@3.5.0/jquery.highlight.js")
        markup.add_script("https://unpkg.com/jquery.scrollto@2.1.3/jquery.scrollTo.js")
        markup.add_script("script.js", items=items)
        markup.add_markup(
            "markup.html",
            target="body",
        )
