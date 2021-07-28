from .exception import LivemarkException
from .system import system


class Snippet:
    def __init__(self, input, *, header, document):
        self.__input = input
        self.__header = header
        self.__document = document
        self.__output = ""

    def __enter__(self):
        assert self.plugin
        return self

    def __exit__(self, type, value, traceback):
        self.bind()

    @property
    def document(self):
        return self.__document

    @property
    def header(self):
        return self.__header

    @property
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    def process(self):
        system.process_snippet(self)

    # Bind

    def bind(self, plugin=None):
        if callable(plugin):
            plugin = plugin.__self__
        self.__plugin = plugin
        return self

    @property
    def plugin(self):
        if not self.__plugin:
            raise LivemarkException("The object is not bound to any plugin")
        return self.__plugin

    @property
    def plugin_config(self):
        return self.document.config.get(self.plugin.name, {})
