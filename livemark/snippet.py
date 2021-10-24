# NOTE:
# We can parse json/yaml in advance for snippet-processing plugins


class Snippet:
    """Livemark snippet

    Parameters:
        input (str): textual snippet for the snippet
        header (str[]): an array of the snippet's header

    """

    def __init__(self, input, *, header):
        lang = ""
        type = ""
        props = {}

        # Infer lang
        if len(header) >= 1:
            lang = header[0].lower()

        # Infer type
        if len(header) >= 2:
            type = header[1].lower()

        # Infer props
        for item in header[2:]:
            parts = item.split("=")
            name = parts[0].lower()
            value = parts[1].lower() if len(parts) == 2 else True
            props[name] = value

        # Set attributes
        self.__input = input
        self.__header = header
        self.__output = None
        self.__lang = lang
        self.__type = type
        self.__props = props

    def __setattr__(self, name, value):
        if name == "output":
            self.__output = value
        elif name == "input":
            self.__input = value
        elif name == "lang":
            self.__lang = value
        elif name == "type":
            self.__type = value
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
        return self.__lang

    @property
    def type(self):
        """Snippet's type

        Returns:
            str: type
        """
        return self.__type

    @property
    def props(self):
        """Snippet's props

        Returns:
            dict: props
        """
        return self.__props

    # Process

    def process(self, document):
        """Process snippet

        Parameters:
            document (Document): document having this snippet
        """
        for plugin in document.plugins:
            plugin.process_snippet(self)
