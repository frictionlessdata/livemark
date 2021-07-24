from ...plugin import Plugin


class BrandPlugin(Plugin):
    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
            config=markup.plugin_config,
        )
