class Snippet:
    def __init__(self, source, *, header):
        self.__source = source
        self.__header = header
        self.__target = ""

    @property
    def header(self):
        return self.__header

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value
