import subprocess
from ...plugin import Plugin


class CleanupPlugin(Plugin):
    priority = -100
    profile = {
        "type": "object",
        "required": ["commands"],
        "properties": {
            "commands": {"type": "array", "items": {"type": "string"}},
        },
    }

    # Process

    def process_config(self, config):
        self.config.setdefault("commands", self.config.pop("self", []))

    def process_document(self, document):
        if self.config:
            for code in self.config["commands"]:
                subprocess.run(code, shell=True)
