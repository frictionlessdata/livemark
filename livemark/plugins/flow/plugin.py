from ...plugin import Plugin


class FlowPlugin(Plugin):
    def process_html(self, markup):
        markup.query("head").append(self.read_asset("style.css"))
        markup.query("#livemark-main").append(
            # TODO: implement prev/next
            self.read_asset("markup.html"),
            data={"prev": {}, "next": {}},
        )
