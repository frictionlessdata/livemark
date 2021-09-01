from ...plugin import Plugin


# NOTE:
# Consider using pure jQuery instead of ue-scroll
# Consider adding help button to teach how to scroll sidebars, shorcuts, etc


class DisplayPlugin(Plugin):
    identity = "display"
    validity = {
        "type": "object",
        "properties": {
            "speed": {"type": "integer"},
        },
    }

    # Context

    @property
    def speed(self):
        return self.config.get("speed", 10)

    # Process

    def process_markup(self, markup):
        url = "https://unpkg.com"
        markup.add_style("style.css")
        markup.add_script(f"{url}/ue-scroll-js@2.0.2/dist/ue-scroll.min.js")
        markup.add_script("script.js")
        markup.add_markup("markup.html", target="body")
