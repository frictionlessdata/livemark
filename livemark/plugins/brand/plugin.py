from ...plugin import Plugin


class BrandPlugin(Plugin):
    priority = 100

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Update markup
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
            config=markup.plugin_config,
            title=markup.document.title,
        )
