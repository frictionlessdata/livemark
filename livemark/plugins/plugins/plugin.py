from ...plugin import Plugin
from ...system import system
from ... import helpers


class PluginsPlugin(Plugin):
    profile = {
        "type": "object",
        "properties": {
            "enable": {
                "type": "array",
                "items": {"type": "string"},
            },
            "disable": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    }

    # Process

    @classmethod
    def process_project(cls, project):
        enable = project.config.get("plugins", {}).get("enable", [])
        disable = project.config.get("plugins", {}).get("disable", [])

        # Init
        Plugins = []
        Plugins.extend(system.builtin)
        Plugins.extend(system.internal)

        # Enable
        for Class in system.external:
            if Class.name in enable:
                Plugins.append(Class)

        # Disable
        for Class in Plugins.copy():
            if Class.name in disable:
                Plugins.remove(Class)

        # Register
        for Class in helpers.order_classes(Plugins, "priority"):
            project.Plugins.append(Class)
