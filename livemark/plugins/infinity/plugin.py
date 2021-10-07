from ...plugin import Plugin


class InfinityPlugin(Plugin):
    identity = "infinity"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
