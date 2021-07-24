from ...plugin import Plugin


# TODO: add scroll support
class PanelPlugin(Plugin):
    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
        markup.add_markup(
            "markup.html",
            target="#livemark-right",
        )
