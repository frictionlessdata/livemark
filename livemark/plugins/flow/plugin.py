from ...plugin import Plugin


class FlowPlugin(Plugin):
    priority = 50

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare prev/next
        prev = None
        next = None
        pages_config = markup.document.config.get("pages")
        if pages_config:
            current_path = "/"
            current_number = None
            if markup.document.target != "index.html":
                current_path = f"/{markup.document.target}"
            for number, link in enumerate(pages_config["list"], start=1):
                if link["path"] == current_path:
                    current_number = number
            if current_number > 1:
                prev = pages_config["list"][current_number - 2]
            if current_number < len(pages_config["list"]):
                next = pages_config["list"][current_number]
        if not next and not prev:
            return

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-main",
            prev=prev,
            next=next,
        )
