import subprocess
from ...plugin import Plugin


class CleanupPlugin(Plugin):
    priority = -10

    def process_document(self, document):
        for code in document.plugin_config.get("cleanup", []):
            subprocess.run(code, shell=True)
