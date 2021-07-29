from ...plugin import Plugin
from ...exception import LivemarkException


class FlowPlugin(Plugin):
    priority = 50

    def process_markup(self, markup):
        config_flow = self.get_config(markup)
        config_pages = self.get_config(markup, plugin="pages")
        if not config_flow or not config_pages:
            return

        # Prepare context
        prev = None
        next = None
        current_path = "/"
        current_number = None
        if markup.document.target != "index.html":
            current_path = f"/{markup.document.target}"
        for number, link in enumerate(config_pages["list"], start=1):
            if link["path"] == current_path:
                current_number = number
        if current_number > 1:
            prev = config_pages["list"][current_number - 2]
        if current_number < len(config_pages["list"]):
            next = config_pages["list"][current_number]
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
