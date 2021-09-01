import subprocess
from ...plugin import Plugin


class CleanupPlugin(Plugin):
    identity = "cleanup"
    priority = -100
    validity = {
        "type": "object",
        "required": ["commands"],
        "properties": {
            "commands": {"type": "array", "items": {"type": "string"}},
        },
    }

    # Context

    @property
    def commands(self):
        return self.config.get("commands", [])

    # Process

    def process_document(self, document):
        for code in self.commands:
            subprocess.run(code, shell=True)
