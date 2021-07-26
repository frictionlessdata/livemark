from ...plugin import Plugin


class PagesPlugin(Plugin):
    priority = 90

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Prepare current
        current = "/"
        if markup.document.target != "index.html":
            current = f"/{markup.document.target}"

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
            config=markup.plugin_config,
            current=current,
        )
