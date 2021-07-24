from pyquery import PyQuery
from .system import system


class Markup:
    def __init__(self, input, *, document):
        self.__input = input
        self.__query = PyQuery(input)
        self.__document = document
        self.__output = ""

    @property
    def input(self):
        return self.__input

    @property
    def query(self):
        return self.__query

    @property
    def document(self):
        return self.__document

    @property
    def output(self):
        return self.__query.html()

    def process(self):
        system.process_markup(self)
