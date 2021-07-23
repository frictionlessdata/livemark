from .system import system


class Snippet:
    def __init__(self, input, *, header, format):
        self.__input = input
        self.__header = header
        self.__format = format
        self.__output = ""

    @property
    def header(self):
        return self.__header

    @property
    def format(self):
        return self.__format

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
        return system.process_snippet(self)
