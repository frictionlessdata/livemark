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
        for code in document.plugin_config.get("cleanup", []):
            subprocess.run(code, shell=True)
