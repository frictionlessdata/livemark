from ...plugin import Plugin


class TocPlugin(Plugin):
    def process_markup(self, markup):
        markup.add_style("https://unpkg.com/tocbot@4.12.3/dist/tocbot.css")
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/tocbot@4.12.3/dist/tocbot.min.js")
        markup.add_script("script.js")
        markup.add_markup(
            "markup.html",
            target="#livemark-left",
        )
