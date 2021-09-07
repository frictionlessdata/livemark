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

    def __setattr__(self, name, value):
        if name == "output":
            self.__output = value
        else:  # default setter
            super().__setattr__(name, value)

    @property
    def input(self):
        """Snippet's input

        Returns:
            str: input
        """
        return self.__input

    @property
    def output(self):
        """Snippet's output

        Returns:
            str?: input
        """
        return self.__output

    @property
    def header(self):
        """Snippet's header

        Returns:
            str[]: header
        """
        return self.__header

    @property
    def lang(self):
        """Snippet's lang

        Returns:
            str: lang
        """
        lang = ""
        if len(self.__header) >= 1:
            lang = self.__header[0].lower()
        return lang

    @property
    def type(self):
        """Snippet's type

        Returns:
            str: type
        """
        type = ""
        if len(self.__header) >= 2:
            type = self.__header[1].lower()
        return type

    @property
    def props(self):
        """Snippet's props

        Returns:
            dict: props
        """
        props = {}
        for item in self.__header[2:]:
            parts = item.split("=")
            name = parts[0].lower()
            value = parts[1].lower() if len(parts) == 2 else True
            props[name] = value
        return props

    # Process

    def process(self, document):
        """Process snippet

        Parameters:
            document (Document): document having this snippet
        """
        for plugin in document.plugins:
            plugin.process_snippet(self)
