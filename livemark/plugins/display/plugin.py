from ...plugin import Plugin


class DisplayPlugin(Plugin):
    priority = 10
    profile = {
        "type": "object",
        "properties": {
            "speed": {"type": "integer"},
        },
    }

    @Plugin.property
    def speed(self):
        return self.config.get("speed", 10)

    # Process

    def process_markup(self, markup):
        if not self.config:
            return

        # Update markup
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/ue-scroll-js@2.0.2/dist/ue-scroll.min.js")
        markup.add_script("script.js", speed=self.speed)
        markup.add_markup(
            "markup.html",
            target="body",
        )
