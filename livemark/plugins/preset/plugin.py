from ...plugin import Plugin
from ...exception import LivemarkException


# TODO: add more presets
# TODO: improve compact preset
# TODO: support setting `preset: {name}` in coinfig without requiring nesting
class PresetPlugin(Plugin):
    priority = 30
    profile = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
    }

    def process_document(self, document):
        config = document.config.get(self.name, {})
        preset = config.get("name", "standard")

        # Update document
        if preset == "standard":
            document.config.setdefault("brand", {"value": True})
            document.config.setdefault("toc", {"value": True})
            document.config.setdefault("stats", {"value": True})
            document.config.setdefault("flow", {"value": True})
            document.config.setdefault("status", {"value": True})
            document.config.setdefault("about", {"value": True})
            document.config.setdefault("links", {"value": True})
            document.config.setdefault("panel", {"value": True})
        elif preset == "compact":
            document.config.setdefault("toc", {"value": True})
            document.config.setdefault("stats", {"value": True})
            document.config.setdefault("flow", {"value": True})
            document.config.setdefault("status", {"value": True})
            document.config.setdefault("links", {"value": True})
            document.config.setdefault("panel", {"value": True})
        else:
            raise LivemarkException(f"Not supported preset: {preset}")
