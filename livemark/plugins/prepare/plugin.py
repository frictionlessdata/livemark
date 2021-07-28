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
        for code in document.plugin_config.get("prepare", []):
            subprocess.run(code, shell=True)
