from ...plugin import Plugin
from ...exception import LivemarkException


class FlowPlugin(Plugin):
    priority = 50

    def process_markup(self, markup):
        pages = self.get_plugin("pages")
        if not self.config or not pages.config:
            return

        # Prepare context
        prev = None
        next = None
        current_path = "/"
        current_number = None
        if self.document.target != "index.html":
            current_path = f"/{markup.document.target}"
        for number, link in enumerate(pages.config["list"], start=1):
            if link["path"] == current_path:
                current_number = number
        if current_number > 1:
            prev = pages.config["list"][current_number - 2]
        if current_number < len(pages.config["list"]):
            next = pages.config["list"][current_number]
        if not next and not prev:
            raise LivemarkException("Invalid pages configuration")

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-main",
            prev=prev,
            next=next,
        )
