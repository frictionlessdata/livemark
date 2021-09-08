from ...plugin import Plugin


# NOTE:
# Add support for many infinity blocks on page
# Add load more button and loading indication?
# Rename and merge with pagination plugin?


class InfinityPlugin(Plugin):
    identity = "infinity"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
