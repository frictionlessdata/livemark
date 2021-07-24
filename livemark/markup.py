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
        # PyQuery uses lxml which esape all the <> inside the tags
        # Here we recover initial formatting for styles and scripts
        lines = []
        is_replacing = False
        output = self.__query.html()
        for line in output.splitlines(keepends=True):
            if line.strip() in ["<style>", "<script>"]:
                is_replacing = True
            elif line.strip() in ["</style>", "</script>"]:
                is_replacing = False
            if is_replacing:
                line = line.replace("&lt;", "<").replace("&gt;", ">")
            lines.append(line)
        return "".join(lines)

    def process(self):
        system.process_markup(self)
