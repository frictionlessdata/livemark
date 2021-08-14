from ...plugin import Plugin
from ...exception import LivemarkException


class SignsPlugin(Plugin):
    priority = 50

    @Plugin.property
    def paths(self):
        pages = self.get_plugin("pages")
        if pages.config:
            prev = None
            next = None
            current_path = "/"
            current_number = None
            if self.document.target != "index.html":
                current_path = f"/{self.document.target}"
            for number, item in enumerate(pages.config["list"], start=1):
                # TODO: Support nested
                if item.get("list"):
                    continue
                if item["path"] == current_path:
                    current_number = number
            if current_number > 1:
                prev = pages.config["list"][current_number - 2]
            if current_number < len(pages.config["list"]):
                next = pages.config["list"][current_number]
            if not next and not prev:
                raise LivemarkException("Invalid pages configuration")
            return {"prev": prev, "next": next}

    # Process

    def process_markup(self, markup):
        # TODO: add property for not self.config (for all plugins)
        if not self.config or not self.paths:
            return

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-main",
            paths=self.paths,
        )
