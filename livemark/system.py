import os
import pkgutil
import importlib
from .helpers import cached_property
from .exception import LivemarkException
from .plugin import Plugin
from . import helpers


# NOTE:
# Investigage the situation when plugins have duplicate names


class System:
    """System for plugin management

    API      | Usage
    -------- | --------
    Public   | `from livemark import system`

    This class provides access to Livemark plugins.
    It's available as `livemark.system` singletone.

    """

    @cached_property
    def builtin(self):
        """Builtin plugin classes

        Returns:
            type[]: a list of plugin classes
        """
        Plugins = []
        module = importlib.import_module("livemark.plugins")
        for _, name, _ in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            module = importlib.import_module(f"livemark.plugins.{name}")
            Plugins.extend(helpers.extract_classes(module, Plugin))
        Plugins = helpers.order_classes(Plugins, "priority")
        return Plugins

    @cached_property
    def internal(self):
        """Internal plugin classes

        Returns:
            type[]: a list of plugin classes
        """
        Plugins = []
        if importlib.util.find_spec("plugin"):
            module = importlib.import_module("plugin")
            Plugins = helpers.extract_classes(module, Plugin)
            Plugins = helpers.order_classes(Plugins, "priority")
        return Plugins

    @cached_property
    def external(self):
        """External plugin classes

        Returns:
            type[]: a list of registered plugin classes
        """
        Plugins = []
        for item in pkgutil.iter_modules():
            if item.name.startswith("livemark_"):
                module = importlib.import_module(item.name)
                Plugins.extend(helpers.extract_classes(module, Plugin))
        Plugins = helpers.order_classes(Plugins, "priority")
        return Plugins

    @cached_property
    def combined(self):
        """Combined plugin classes

        Returns:
            type[]: a list of registered plugin classes
        """
        Plugins = self.builtin + self.internal + self.external
        Plugins = helpers.order_classes(Plugins, "priority")
        return Plugins

    def register(self, Plugin):
        """Register a plugin

        Parameters:
            Plugin (type): a plugin class to register
        """
        self.internal.append(Plugin)
        self.internal = helpers.order_classes(self.internal, "priority")

    def deregister(self, Plugin):
        """Register a plugin

        Parameters:
            Plugin (type): a plugin class to register
        """
        try:
            self.internal.remove(Plugin)
        except ValueError:
            raise LivemarkException(f"Not registered plugin: {Plugin}")


system = System()
