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
        if not self.config:
            return

        # Prepare document
        for code in self.config:
            subprocess.run(code, shell=True)
