from ...plugin import Plugin


class CounterPlugin(Plugin):
    def process_markup(self, markup):
        if not markup.plugin_config:
            return

        # Update markup
        if markup.plugin_config.get("type") == "google":
            markup.add_markup(
                "markup.html",
                target="head",
                config=markup.plugin_config,
            )
