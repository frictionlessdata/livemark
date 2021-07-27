from ...plugin import Plugin
from ...exception import LivemarkException


# TODO: add more presets
# TODO: support setting `preset: {name}` with no nesting
class PresetPlugin(Plugin):
    def prepare_document(self, document):
        name = document.plugin_config.get("name", "standard")
        if name == "standard":
            document.config.setdefault("brand", True)
            document.config.setdefault("toc", True)
            document.config.setdefault("stats", True)
            document.config.setdefault("flow", True)
            document.config.setdefault("status", True)
            document.config.setdefault("about", True)
            document.config.setdefault("links", True)
            document.config.setdefault("panel", True)
        # TODO: improve this preset
        elif name == "compact":
            document.config.setdefault("toc", True)
            document.config.setdefault("stats", True)
            document.config.setdefault("flow", True)
            document.config.setdefault("status", True)
            document.config.setdefault("links", True)
            document.config.setdefault("panel", True)
        else:
            raise LivemarkException(f"Not supported preset: {name}")
