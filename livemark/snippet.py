from .helpers import cached_property


class Snippet:
    """Livemark snippet

    API      | Usage
    -------- | --------
    Public   | `from livemark import Snippet`

    Parameters:
        input (str): textual snippet for the snippet
        header (str[]): an array of the snippet's header

    """

    def __init__(self, input, *, header):
        self.__input = input
        self.__header = header
        self.__output = None

    @property
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @property
    def header(self):
        return self.__header

    @cached_property
    def lang(self):
        lang = None
        if len(self.__header) >= 1:
            lang = self.__header[0]
        return lang

    @cached_property
    def type(self):
        type = None
        if len(self.__header) >= 2:
            type = self.__header[1]
        return type

    @cached_property
    def mode(self):
        mode = None
        if len(self.__header) >= 3:
            mode = self.__header[2]
        return mode

    # Process

    def process(self, document):
        for plugin in document.plugins:
            plugin.process_snippet(self)
