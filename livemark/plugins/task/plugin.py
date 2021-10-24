from ... import Plugin


class TaskPlugin(Plugin):
    identity = "task"

    def process_markup(self, markup):
        markup.add_style("style.css")
