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
        config = self.get_config(document)
        if not config:
            return

        # Cleaup document
        for code in config:
            subprocess.run(code, shell=True)
