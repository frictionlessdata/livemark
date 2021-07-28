from ...plugin import Plugin


class PagesPlugin(Plugin):
    priority = 90

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare context
        current = "/"
        if markup.document.target != "index.html":
            current = f"/{markup.document.target}"
        list = markup.plugin_config["list"]

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
            current=current,
            list=list,
        )
