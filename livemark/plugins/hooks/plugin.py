import subprocess
from ...plugin import Plugin


class HooksPlugin(Plugin):
    def prepare_document(self, document):
        for code in document.plugin_config.get("prepare", []):
            subprocess.run(code, shell=True)

    def cleanup_document(self, document):
        for code in document.plugin_config.get("cleanup", []):
            subprocess.run(code, shell=True)
