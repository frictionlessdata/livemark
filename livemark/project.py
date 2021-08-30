from .config import Config
from .exception import LivemarkException
from .system import system
from . import settings


# NOTE:
# Review whether it's right to read all the documents on init (duplicate with document?)
# We read them to get access to configs and iferred data


class Project:
    def __init__(self, document=None, *, config=None, format=None):
        self.__documents = [document] if document else []
        self.__config = Config(config)
        self.__document = document
        self.__format = format

        # Process project
        for Plugin in system.iterate():
            type = Plugin.get_type()
            internal = type == "internal" and Plugin.name not in self.__config.disable
            external = type == "external" and Plugin.name in self.__config.enable
            if internal or external:
                Plugin.process_project(self)

        # Read documents
        for document in self.__documents:
            document.project = self
            document.read()

    @property
    def format(self):
        if self.__format:
            return self.__format
        if self.__document:
            return self.__document.format
        return settings.DEFAULT_FORMAT

    @property
    def config(self):
        return self.__config

    @property
    def document(self):
        return self.__document

    @property
    def documents(self):
        return self.__documents

    @property
    def building_documents(self):
        return [self.document] if self.document else self.documents

    # Build

    def build(self, *, diff=False, print=False):

        # Ensure documents
        if not self.documents:
            raise LivemarkException("No documents to build in the project")

        # Build documents
        outputs = []
        for document in self.building_documents:
            output = document.build(diff=diff, print=print)
            if output:
                outputs.append(output)
        output = "\n".join(outputs)

        return output
