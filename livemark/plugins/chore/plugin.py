import subprocess
from ...plugin import Plugin


class ChorePlugin(Plugin):
    def prepare_document(self, document):
        for code in document.config.get("chore", {}).get("prepare", []):
            subprocess.run(code, shell=True)

    def cleanup_document(self, document):
        for code in document.config.get("chore", {}).get("cleanup", []):
            subprocess.run(code, shell=True)
