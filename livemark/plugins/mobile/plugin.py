from ...plugin import Plugin


# This plugin is based on the following article:
# https://dev.to/devggaurav/let-s-build-a-responsive-navbar-and-hamburger-menu-using-html-css-and-javascript-4gci


class MobilePlugin(Plugin):
    # TODO: update all the priorities (maybe group by column/section?)
    priority = 10

    def process_markup(self, markup):

        # Update markup
        markup.add_style("style.css")
        markup.add_script("script.js")
        markup.add_markup("markup.html")
