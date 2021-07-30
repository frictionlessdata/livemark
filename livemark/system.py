import os
import pkgutil
from importlib import import_module
from .helpers import cached_property
from .exception import LivemarkException
from .plugin import Plugin


class System:
    """System representation

    API      | Usage
    -------- | --------
    Public   | `from livemark import system`

    This class provides asses to Livemark plugins.
    It's available as `livemark.system` singletone.

    """

    @cached_property
    def Plugins(self):
        """Plugin classes

        Returns:
            type[]: a list of registered plugin classes
        """
        Plugins = []
        modules = []
        for item in pkgutil.iter_modules():
            if item.name == "plugin" or item.name.startswith("livemark_"):
                module = import_module(item.name)
                modules.append(module)
        module = import_module("livemark.plugins")
        for _, name, _ in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            module = import_module(f"livemark.plugins.{name}")
            modules.append(module)
        for module in modules:
            for item in vars(module).values():
                if isinstance(item, type) and issubclass(item, Plugin):
                    Plugins.append(item)
        return list(sorted(Plugins, key=lambda Plugin: -Plugin.priority))

    def register(self, Plugin):
        """Register a plugin

        Parameters:
            Plugin (type): a plugin class to register
        """
        for index, Class in list(enumerate(self.Plugins)):
            if Plugin.priority >= Class.priority:
                self.Plugins.insert(index, Plugin)

    def deregister(self, Plugin):
        """Register a plugin

        Parameters:
            Plugin (type): a plugin class to register
        """
        try:
            self.Plugins.remove(Plugin)
        except ValueError:
            raise LivemarkException(f"Not registered plugin: {Plugin}")


system = System()
