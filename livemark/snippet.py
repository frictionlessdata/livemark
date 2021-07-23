from .system import system


class Snippet:
    def __init__(self, input, *, header):
        self.__input = input
        self.__header = header
        self.__output = ""

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
        return system.process_snippet(self)
