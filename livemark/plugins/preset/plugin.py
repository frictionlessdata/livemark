from ...plugin import Plugin
from ...exception import LivemarkException


# NOTE:
# We need to add more presets and improve existent ones
# For example, we can make "compact" preset more minimalistic
class PresetPlugin(Plugin):
    profile = {
        "type": "object",
        "requried": ["name"],
        "properties": {
            "name": {"type": "string"},
        },
    }

    def process_config(self, config):
        preset = self.config.setdefault("name", self.config.get("self", "standard"))

        # Update document
        if preset == "standard":
            config["brand"]["self"] = True
            config["toc"]["self"] = True
            config["stats"]["self"] = True
            config["signs"]["self"] = True
            config["rating"]["self"] = True
            config["about"]["self"] = True
            config["links"]["self"] = True
            config["controls"]["self"] = True
        elif preset == "compact":
            config["toc"]["self"] = True
            config["stats"]["self"] = True
            config["signs"]["self"] = True
            config["rating"]["self"] = True
            config["links"]["self"] = True
            config["controls"]["self"] = True
        else:
            raise LivemarkException(f"Not supported preset: {preset}")
