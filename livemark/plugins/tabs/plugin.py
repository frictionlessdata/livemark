from ...plugin import Plugin


class TabsPlugin(Plugin):
    identity = "tabs"

    # Process

    def process_markup(self, markup):
        if self.document.format == "html":
            markup.add_style("style.css")

            # Collect sources
            number = 1
            groups = {}
            sources = list(markup.query("[data-tabs]").items())
            for source in sources:
                name = source.attr("data-tabs")
                id = f"livemark-tabs-{number}-{name}"
                tab = dict(id=id, name=name, content=source.html(), markup=source)
                groups.setdefault(number, [])
                groups[number].append(tab)
                if not source.next().attr("data-tabs"):
                    number += 1

            # Render sources
            for tabs in groups.values():
                output = self.read_asset("markup.html", tabs=tabs)
                tabs[0]["markup"].after(output)

            # Delete sources
            markup.query("[data-tabs]").remove()
