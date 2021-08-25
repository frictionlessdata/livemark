from ...plugin import Plugin


class SignsPlugin(Plugin):
    name = "signs"
    priority = 40

    # Context

    @Plugin.property
    def items(self):
        pages = self.document.get_plugin("pages")
        if pages and pages.items:
            prev = None
            next = None
            current_number = None
            for number, item in enumerate(pages.flatten_items, start=1):
                if item["path"] == self.document.path:
                    current_number = number
            if current_number:
                if current_number > 1:
                    prev = pages.flatten_items[current_number - 2]
                if current_number < len(pages.flatten_items):
                    next = pages.flatten_items[current_number]
            return {"prev": prev, "next": next}

    # Process

    def process_markup(self, markup):
        if self.items:
            markup.add_style("style.css")
            markup.add_markup("markup.html", target="#livemark-main")
