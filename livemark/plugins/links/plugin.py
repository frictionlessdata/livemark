from ...plugin import Plugin


class LinksPlugin(Plugin):
    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
            config=markup.plugin_config,
        )
