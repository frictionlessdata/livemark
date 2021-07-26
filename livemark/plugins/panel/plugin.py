from ...plugin import Plugin


class PanelPlugin(Plugin):
    priority = 10

    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Update markup
        markup.add_style("https://unpkg.com/ue-scroll-js@2.0.2/dist/ue-scroll.min.css")
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/ue-scroll-js@2.0.2/dist/ue-scroll.min.js")
        markup.add_script("script.js", config=markup.plugin_config)
        markup.add_markup(
            "markup.html",
            target="body",
        )
