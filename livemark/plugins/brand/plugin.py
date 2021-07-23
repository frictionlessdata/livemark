from ...plugin import Plugin


class BrandPlugin(Plugin):
    def process_html(self, markup):
        config = markup.document.config
        markup.query("head").append(self.read_asset("style.css", tag="style"))
        markup.query("#livemark-left").append(
            self.read_asset("markup.html", data={"title": config.brand.title})
        )
