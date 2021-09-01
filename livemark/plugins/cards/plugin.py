from jinja2 import Template
from ...plugin import Plugin
from ... import helpers


# NOTE:
# We'd like to support rendering cards from markdown sources
# We need to provide a lightweigh redering mechanism for Document to achieve it


class CardsPlugin(Plugin):
    identity = "cards"

    # Process

    def process_markup(self, markup):
        markup.add_style("style.css")
        markup.add_script("script.js")
        markup.add_markup("markup.html")

    # Helpers

    @staticmethod
    def create_card(source, *, code, **context):
        target = f"assets/cards/{code}.html"
        with open(source) as file:
            template = Template(file.read().strip(), trim_blocks=True)
            text = template.render(**context)
        helpers.write_file(target, text)

    @staticmethod
    def delete_cards():
        target = "assets/cards"
        helpers.remove_dir(target)
