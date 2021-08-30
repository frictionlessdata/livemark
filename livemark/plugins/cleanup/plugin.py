import subprocess
from ...plugin import Plugin


class CleanupPlugin(Plugin):
    code = "cleanup"
    priority = -100
    profile = {
        "type": "object",
        "required": ["commands"],
        "properties": {
            "commands": {"type": "array", "items": {"type": "string"}},
        },
    }

    # Context

    @Plugin.property
    def commands(self):
        return self.config.get("commands", [])

    # Process

    def process_document(self, document):
        for code in self.commands:
            subprocess.run(code, shell=True)
