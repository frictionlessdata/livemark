from ...plugin import Plugin


class TocPlugin(Plugin):
    def process_markup(self, markup):
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("body").append(self.read_asset("script.js", tag="script"))
        markup.query("#livemark-left").append(self.read_asset("markup.html"))
