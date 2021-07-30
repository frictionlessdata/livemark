import subprocess
from ...plugin import Plugin


class PreparePlugin(Plugin):
    priority = 110
    profile = {
        "type": "object",
        "required": ["commands"],
        "properties": {
            "commands": {"type": "array", "items": {"type": "string"}},
        },
    }

    def process_config(self, config):
        self.config.setdefault("commands", self.config.pop("self", []))

    def process_document(self, document):
        if not self.config:
            return

        # Prepare document
        for code in self.config["commands"]:
            subprocess.run(code, shell=True)
