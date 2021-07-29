from ...plugin import Plugin
from ...exception import LivemarkException


# TODO: add more presets
# TODO: improve compact preset
# TODO: support setting `preset: {name}` in config without requiring nesting
class PresetPlugin(Plugin):
    priority = 30
    profile = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
    }

    def process_document(self, document):
        preset = self.config.get("name", "standard")

        # Update document
        if preset == "standard":
            document.config["brand"]["value"] = True
            document.config["toc"]["value"] = True
            document.config["stats"]["value"] = True
            document.config["flow"]["value"] = True
            document.config["status"]["value"] = True
            document.config["about"]["value"] = True
            document.config["links"]["value"] = True
            document.config["panel"]["value"] = True
        elif preset == "compact":
            document.config["toc"]["value"] = True
            document.config["stats"]["value"] = True
            document.config["flow"]["value"] = True
            document.config["status"]["value"] = True
            document.config["links"]["value"] = True
            document.config["panel"]["value"] = True
        else:
            raise LivemarkException(f"Not supported preset: {preset}")
