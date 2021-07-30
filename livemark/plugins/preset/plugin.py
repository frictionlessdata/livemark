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
        self.config.setdefault("name", self.config.get("self", "standard"))

        # Update document
        if self.config["name"] == "standard":
            config["brand"]["self"] = True
            config["toc"]["self"] = True
            config["stats"]["self"] = True
            config["flow"]["self"] = True
            config["rating"]["self"] = True
            config["about"]["self"] = True
            config["links"]["self"] = True
            config["panel"]["self"] = True
        elif self.config["name"] == "compact":
            config["toc"]["self"] = True
            config["stats"]["self"] = True
            config["flow"]["self"] = True
            config["rating"]["self"] = True
            config["links"]["self"] = True
            config["panel"]["self"] = True
        else:
            raise LivemarkException(f"Not supported preset: {self.config['name']}")
