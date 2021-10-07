from ...project import Project
from ...plugin import Plugin
from ... import helpers


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
        project = Project(source, target=target, config={"site": False})
        project.document.read()
        project.document.get_plugin("logic").context.update(code=code)
        project.document.get_plugin("logic").context.update(context)
        project.document.build()

    @staticmethod
    def delete_cards():
        target = "assets/cards"
        helpers.remove_dir(target)
