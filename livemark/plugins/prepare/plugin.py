import subprocess
from ...plugin import Plugin


class PreparePlugin(Plugin):
    priority = 40
    profile = {
        "type": "array",
        "items": {
            "type": "string",
        },
    }

    def process_document(self, document):
        config = document.config.get(self.name, {})
        if not config:
            return

        # Prepare document
        for code in config:
            subprocess.run(code, shell=True)
