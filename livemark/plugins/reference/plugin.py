from ...plugin import Plugin


class ReferencePlugin(Plugin):
    identity = "reference"
    priority = 60

    # Process

    def process_snippet(self, snippet):
        pass
