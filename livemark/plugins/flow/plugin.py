from ...plugin import Plugin


class FlowPlugin(Plugin):
    priority = 50

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_markup(
            "markup.html",
            target="#livemark-main",
            # TODO: implement prev/next
            prev={},
            next={},
        )
