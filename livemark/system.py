import os
import pkgutil
from collections import OrderedDict
from importlib import import_module
from .helpers import cached_property


class System:
    """System representation

    API      | Usage
    -------- | --------
    Public   | `from livemark import system`

    This class provides an ability to make system Livemark calls.
    It's available as `livemark.system` singletone.

    """

    def __init__(self):
        self.__dynamic_plugins = OrderedDict()

    def register(self, name, plugin):
        """Register a plugin

        Parameters:
            name (str): plugin name
            plugin (Plugin): plugin to register
        """
        self.__dynamic_plugins[name] = plugin
        if "methods" in self.__dict__:
            del self.__dict__["plugins"]
            del self.__dict__["methods"]

    # Actions

    actions = [
        "process_html",
        "process_snippet",
        "process_config",
        "process_document",
    ]

    def process_html(self, html):
        """Process html

        Parameters:
            html (object): pyquery document

        Returns:
            object: processed pyquery document
        """
        for func in self.methods["process_html"].values():
            html = func(html)
        return html

    def process_snippet(self, snippet):
        """Process snippet

        Parameters:
            code (object): code object

        Returns:
            object: code object
        """
        for func in self.methods["process_snippet"].values():
            snippet = func(snippet)
        return snippet

    def process_config(self, config):
        """Process config

        Parameters:
            config (object): config object

        Returns:
            object: config object
        """
        for func in self.methods["process_config"].values():
            config = func(config)
        return config

    def process_document(self, document):
        """Process document

        Parameters:
            document (object): document object

        Returns:
            object: document object
        """
        for func in self.methods["process_document"].values():
            document = func(document)
        return document

    # Methods

    @cached_property
    def methods(self):
        methods = {}
        for action in self.actions:
            methods[action] = OrderedDict()
            for name, plugin in self.plugins.items():
                if action in vars(type(plugin)):
                    func = getattr(plugin, action, None)
                    methods[action][name] = func
        return methods

    # Plugins

    @cached_property
    def plugins(self):
        modules = OrderedDict()
        for item in pkgutil.iter_modules():
            if item.name.startswith("livemark_"):
                module = import_module(item.name)
                modules[item.name.replace("livemark_", "")] = module
        module = import_module("livemark.plugins")
        for _, name, _ in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            module = import_module(f"livemark.plugins.{name}")
            modules[name] = module
        plugins = OrderedDict(self.__dynamic_plugins)
        for name, module in modules.items():
            Plugin = getattr(module, f"{name.capitalize()}Plugin", None)
            if Plugin:
                plugin = Plugin()
                plugins[name] = plugin
        return plugins


system = System()
