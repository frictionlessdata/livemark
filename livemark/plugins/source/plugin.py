from ...plugin import Plugin


class SourcePlugin(Plugin):
    identity = "source"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
