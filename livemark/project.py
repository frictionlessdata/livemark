from .system import system
from .config import Config
from .exception import LivemarkException
from .helpers import cached_property


class Project:
    def __init__(self, *, config=None):
        self.__config = Config(config)
        self.__documents = []
        for Plugin in system.Plugins:
            Plugin.process_project(self)

    @cached_property
    def config(self):
        return self.__config

    @cached_property
    def documents(self):
        return self.__documents

    # Helpers

    def get_document(self, path):
        for document in self.__documents:
            if document.path == path:
                return document
        raise LivemarkException(f"There is no document: {path}")
