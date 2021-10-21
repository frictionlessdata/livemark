from ...plugin import Plugin


# NOTE:
# Consider using proper markdown parser client-side
# Or embed source generation in the server-side chain


class SourcePlugin(Plugin):
    identity = "source"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
