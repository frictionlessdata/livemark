import os
import pkgutil
import importlib
from cached_property import cached_property
from .plugin import Plugin
from . import helpers
from . import errors


class System:
    """System for plugin management

    API      | Usage
    -------- | --------
    Public   | `from livemark import system`

    This class provides access to Livemark plugins.
    It's available as `livemark.system` singletone.

    """

    @cached_property
    def Plugins(self):
        """Registered plugins

        Returns:
            dict: plugins mapping
        """
        Plugins = {}
        modules = []
        for item in pkgutil.iter_modules():
            if item.name in ["plugin", "plugins"] or item.name.startswith("livemark_"):
                module = importlib.import_module(item.name)
                modules.append(module)
        module = importlib.import_module("livemark.plugins")
        for _, name, _ in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            module = importlib.import_module(f"livemark.plugins.{name}")
            modules.append(module)
        for module in modules:
            for Class in helpers.extract_classes(module, Plugin):
                if Class.identity in Plugins:
                    raise errors.Error(f"Plugin name conflict: {Class.identity}")
                Plugins[Class.identity] = Class
        return Plugins

    # Manage

    def iterate(self):
        """Iterate plugins by priority

        Returns:
            type[]: list of plugin classes
        """
        objects = self.Plugins.values()
        return helpers.order_objects(objects, "priority")

    def register(self, Plugin):
        """Register a plugin

        Parameters:
            Plugin (type): a plugin class to register
        """
        if Plugin.identity in self.Plugins:
            raise errors.Error(f"Plugin name conflict: {Plugin.identity}")
        self.Plugins[Plugin.identity] = Plugin

    def deregister(self, Plugin):
        """Deregister a plugin

        Parameters:
            Plugin (type): a plugin class to register
        """
        if Plugin.identity not in self.Plugins:
            raise errors.Error(f"Not registered plugin: {Plugin.identity}")
        del self.Plugins[Plugin.identity]


system = System()
