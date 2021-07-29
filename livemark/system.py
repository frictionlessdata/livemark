import os
import pkgutil
from collections import OrderedDict
from importlib import import_module


class System:
    """System representation

    API      | Usage
    -------- | --------
    Public   | `from livemark import system`

    This class provides asses to Livemark plugins.
    It's available as `livemark.system` singletone.

    """

    def __init__(self):

        # Collect modules
        modules = OrderedDict()
        for item in pkgutil.iter_modules():
            if item.name == "plugin" or item.name.startswith("livemark_"):
                module = import_module(item.name)
                modules[item.name.replace("livemark_", "")] = module
        module = import_module("livemark.plugins")
        for _, name, _ in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            module = import_module(f"livemark.plugins.{name}")
            modules[name] = module

        # Collect plugins
        Plugins = []
        for name, module in modules.items():
            Plugin = getattr(module, f"{name.capitalize()}Plugin", None)
            if Plugin:
                Plugins.append(Plugin)
        Plugins = list(sorted(Plugins, key=lambda Plugin: -Plugin.priority))

        # Set attributes
        self.__modules = modules
        self.__Plugins = Plugins

    def register_plugin(self, Plugin):
        """Register a plugin

        Parameters:
            Plugin (class): a plugin class to register
        """
        for index, Class in list(enumerate(self.__Plugins)):
            if Plugin.priority >= Class.priority:
                self.Plugins.insert(index, Plugin)

    def create_plugins(self, document):
        """Create plugin instances

        Parameters:
            document (Document): a document object

        Returns:
            Plugin[]: a list of plugin instances
        """
        return list(map(lambda Plugin: Plugin(document), self.__Plugins))


system = System()
