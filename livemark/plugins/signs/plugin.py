from ...plugin import Plugin
from ... import helpers


# NOTE:
# review why we check that self.document.project exists in items


class SignsPlugin(Plugin):
    identity = "signs"
    priority = 40

    # Context

    @property
    def current(self):
        return self.document.path

    @property
    def items(self):
        if self.document.project:
            documents = self.document.project.documents
            if documents:
                prev = None
                next = None
                current_number = None
                for number, document in enumerate(documents, start=1):
                    if document.path == self.document.path:
                        current_number = number
                if current_number:
                    if current_number > 1:
                        document = documents[current_number - 2]
                        path = helpers.get_url_relpath(document.path, self.current)
                        prev = {"name": document.name, "path": path}
                    if current_number < len(documents):
                        document = documents[current_number]
                        path = helpers.get_url_relpath(document.path, self.current)
                        next = {"name": document.name, "path": path}
                return {"prev": prev, "next": next}

    # Process

    def process_markup(self, markup):
        if self.items:
            markup.add_style("style.css")
            markup.add_markup("markup.html", target="#livemark-main")
