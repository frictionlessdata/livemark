from .system import system


class Snippet:
    def __init__(self, input, *, header, document):
        self.__input = input
        self.__header = header
        self.__document = document
        self.__output = None

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
