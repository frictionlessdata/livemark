from ...plugin import Plugin


class DisplayPlugin(Plugin):
    profile = {
        "type": "object",
        "properties": {
            "speed": {"type": "integer"},
        },
    }

    # Context

    @Plugin.property
    def speed(self):
        return self.config.get("speed", 10)

    # Process

    def process_markup(self, markup):
        if self.config:
            url = "https://unpkg.com"
            markup.add_style("style.css")
            markup.add_script(f"{url}/ue-scroll-js@2.0.2/dist/ue-scroll.min.js")
            markup.add_script("script.js", speed=self.speed)
            markup.add_markup(
                "markup.html",
                target="body",
            )
