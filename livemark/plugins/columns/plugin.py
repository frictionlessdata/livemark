from ...plugin import Plugin


class ColumnsPlugin(Plugin):
    identity = "columns"

    # Process

    def process_markup(self, markup):
        if self.document.format == "html":

            # Collect sources
            number = 1
            groups = {}
            sources = list(markup.query("[data-columns]").items())
            for source in sources:
                column = dict(content=source.html(), markup=source)
                groups.setdefault(number, [])
                groups[number].append(column)
                if not source.next().attr("data-columns"):
                    number += 1

            # Render sources
            for columns in groups.values():
                output = self.read_asset("markup.html", columns=columns)
                columns[0]["markup"].after(output)

            # Delete sources
            markup.query("[data-columns]").remove()
