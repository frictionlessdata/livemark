from ...plugin import Plugin


# TODO: add scroll support
class PanelPlugin(Plugin):
    def process_html(self, markup):
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("body").append(self.read_asset("script.js", tag="script"))
        markup.query("#livemark-right").append(self.read_asset("markup.html"))
