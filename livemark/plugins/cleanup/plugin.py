import subprocess
from ...plugin import Plugin


class CleanupPlugin(Plugin):
    def cleanup_document(self, document):
        for code in document.plugin_config.get("cleanup", []):
            subprocess.run(code, shell=True)
