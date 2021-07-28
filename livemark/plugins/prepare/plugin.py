import subprocess
from ...plugin import Plugin


class PreparePlugin(Plugin):
    def prepare_document(self, document):
        for code in document.plugin_config.get("prepare", []):
            subprocess.run(code, shell=True)
