from ...plugin import Plugin


class ControlsPlugin(Plugin):
    priority = 10
    profile = {
        "type": "object",
        "properties": {
            "speed": {"type": "integer"},
        },
    }

    def process_markup(self, markup):
        if not self.config:
            return

        # Prepare context
        speed = self.config.get("speed", 10)

        # Update markup
        markup.add_style("https://unpkg.com/ue-scroll-js@2.0.2/dist/ue-scroll.min.css")
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/ue-scroll-js@2.0.2/dist/ue-scroll.min.js")
        markup.add_script("script.js", speed=speed)
        markup.add_markup(
            "markup.html",
            target="body",
        )
