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

    @property
    def language(self):
        language = None
        if len(self.__header) >= 1:
            language = self.__header[0]
        return language

    @property
    def modifier(self):
        modifier = None
        if len(self.__header) >= 2:
            modifier = self.__header[1]
        return modifier

    # Process

    def process(self, document):
        for plugin in document.plugins:
            plugin.process_snippet(self)
