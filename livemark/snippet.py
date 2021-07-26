from .system import system


# TODO: add access to document instead for format?
class Snippet:
    def __init__(self, input, *, format, header):
        self.__input = input
        self.__format = format
        self.__header = header
        self.__output = ""

    @property
    def format(self):
        return self.__format

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
