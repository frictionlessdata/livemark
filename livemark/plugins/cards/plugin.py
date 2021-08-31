from jinja2 import Template
from ...plugin import Plugin
from ... import helpers


class CardsPlugin(Plugin):
    code = "cards"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
        markup.add_markup("markup.html")

    # Helpers

    @staticmethod
    def create_card(source, *, code, **context):
        target = f".livemark/cards/{code}.html"
        with open(source) as file:
            template = Template(file.read().strip(), trim_blocks=True)
            text = template.render(**context)
        helpers.write_file(target, text)

    @staticmethod
    def remove_cards():
        target = ".livemark/cards"
        helpers.remove_dir(target)
