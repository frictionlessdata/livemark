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

    # Process

    def process_config(self, config):
        preset = self.config.setdefault("name", self.config.get("self", "standard"))

        # Standard preset
        if preset == "standard":
            config["brand"]["self"] = True
            config["topics"]["self"] = True
            config["search"]["self"] = True
            config["notes"]["self"] = True
            config["signs"]["self"] = True
            config["rating"]["self"] = True
            config["about"]["self"] = True
            config["links"]["self"] = True
            config["display"]["self"] = True
            return

        # Compact preset
        elif preset == "compact":
            config["topics"]["self"] = True
            config["search"]["self"] = True
            config["notes"]["self"] = True
            config["signs"]["self"] = True
            config["rating"]["self"] = True
            config["links"]["self"] = True
            config["display"]["self"] = True
            return

        # Not supported
        raise LivemarkException(f"Not supported preset: {preset}")
