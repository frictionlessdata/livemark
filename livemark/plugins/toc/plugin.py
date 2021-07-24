from ...plugin import Plugin


class TocPlugin(Plugin):
    def process_markup(self, markup):
        markup.query("head").append(
            '<link rel="stylesheet" href="https://unpkg.com/tocbot@4.12.3/dist/tocbot.css">\n'
        )
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("body").append(
            '<script src="https://unpkg.com/tocbot@4.12.3/dist/tocbot.min.js"></script>\n'
        )
        markup.query("body").append(self.read_asset("script.js", tag="script"))
        markup.query("#livemark-left").append(self.read_asset("markup.html"))
