from ...plugin import Plugin


# NOTE:
# Add an ability to customize selector in the config
# Fix how pagination navs are styles (conflict with the main styles)
# Support multiple containers


class PaginationPlugin(Plugin):
    identity = "pagination"

    # Process

    def process_markup(self, markup):
        markup.add_style("https://unpkg.com/paginationjs@2.1.5/dist/pagination.css")
        markup.add_style("style.css")
        markup.add_script("https://unpkg.com/paginationjs@2.1.5/dist/pagination.min.js")
        markup.add_script("script.js")
