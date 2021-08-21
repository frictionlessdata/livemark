from ...plugin import Plugin
from ...exception import LivemarkException


class SignsPlugin(Plugin):
    priority = 40

    # Context

    @Plugin.property
    def paths(self):
        pages = self.document.get_plugin("pages")
        if pages.config:
            prev = None
            next = None
            current_path = "/"
            current_number = None
            if self.document.target != "index.html":
                current_path = f"/{self.document.target}"
            for number, item in enumerate(pages.items_flatten, start=1):
                if item["path"] == current_path:
                    current_number = number
            if current_number > 1:
                prev = pages.items_flatten[current_number - 2]
            if current_number < len(pages.items_flatten):
                next = pages.items_flatten[current_number]
            if not next and not prev:
                raise LivemarkException("Invalid pages configuration")
            return {"prev": prev, "next": next}

    # Process

    def process_markup(self, markup):
        if self.config and self.paths:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-main",
                paths=self.paths,
            )
