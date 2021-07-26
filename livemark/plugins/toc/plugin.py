from ...plugin import Plugin


class TocPlugin(Plugin):
    priority = 80

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Update markup
        markup.add_style("https://unpkg.com/tocbot@4.12.3/dist/tocbot.css")
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/tocbot@4.12.3/dist/tocbot.min.js")
        markup.add_script("script.js", config=markup.plugin_config)
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
        )
