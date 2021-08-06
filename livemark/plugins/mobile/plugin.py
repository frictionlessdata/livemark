from ...plugin import Plugin


class MobilePlugin(Plugin):
    # TODO: update all the priorities (maybe group by column/section?)
    priority = 55

    def process_markup(self, markup):

        # Update markup
        markup.add_style("style.css")
        markup.add_script("script.js")
        markup.add_markup(
            "markup.html",
            action="prepend",
            target="#livemark-main",
        )
