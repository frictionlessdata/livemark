from ...plugin import Plugin


class PaginationPlugin(Plugin):
    identity = "pagination"

    # Process

    def process_markup(self, markup):
        markup.add_style("https://unpkg.com/paginationjs@2.1.5/dist/pagination.css")
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/paginationjs@2.1.5/dist/pagination.min.js")
        markup.add_script("script.js")
