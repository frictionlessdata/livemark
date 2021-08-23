from ...plugin import Plugin
from ...exception import LivemarkException


class SignsPlugin(Plugin):
    priority = 40

    # Context

    @Plugin.property
    def paths(self):
        pages = self.document.get_plugin("pages")
        if pages:
            prev = None
            next = None
            current_number = None
            for number, item in enumerate(pages.flatten_items, start=1):
                if item["path"] == self.document.path:
                    current_number = number
            if not current_number:
                raise LivemarkException("Invalid pages configuration")
            if current_number > 1:
                prev = pages.flatten_items[current_number - 2]
            if current_number < len(pages.flatten_items):
                next = pages.flatten_items[current_number]
            return {"prev": prev, "next": next}

    # Process

    def process_markup(self, markup):
        if self.paths:
            markup.add_style("style.css")
            markup.add_markup(
                "markup.html",
                target="#livemark-main",
                paths=self.paths,
            )
