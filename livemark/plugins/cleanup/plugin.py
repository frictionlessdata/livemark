import subprocess
from ...plugin import Plugin


class CleanupPlugin(Plugin):
    priority = -10
    profile = {
        "type": "array",
        "items": {
            "type": "string",
        },
    }

    def process_document(self, document):
        if not self.config:
            return

        # Cleaup document
        for code in self.config:
            subprocess.run(code, shell=True)
