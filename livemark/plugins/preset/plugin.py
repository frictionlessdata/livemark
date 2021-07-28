from ...plugin import Plugin
from ...exception import LivemarkException


# TODO: add more presets
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
        name = document.plugin_config.get("name", "standard")
        if name == "standard":
            document.config.setdefault("brand", {"value": True})
            document.config.setdefault("toc", {"value": True})
            document.config.setdefault("stats", {"value": True})
            document.config.setdefault("flow", {"value": True})
            document.config.setdefault("status", {"value": True})
            document.config.setdefault("about", {"value": True})
            document.config.setdefault("links", {"value": True})
            document.config.setdefault("panel", {"value": True})
        # TODO: improve this preset
        elif name == "compact":
            document.config.setdefault("toc", {"value": True})
            document.config.setdefault("stats", {"value": True})
            document.config.setdefault("flow", {"value": True})
            document.config.setdefault("status", {"value": True})
            document.config.setdefault("links", {"value": True})
            document.config.setdefault("panel", {"value": True})
        else:
            raise LivemarkException(f"Not supported preset: {name}")
