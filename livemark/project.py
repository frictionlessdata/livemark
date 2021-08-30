from .config import Config
from .exception import LivemarkException
from .system import system
from . import settings


class Project:
    def __init__(self, document=None, *, config=None, format=None):
        self.__documents = [document] if document else []
        self.__config = Config(config)
        self.__document = document
        self.__format = format

        # Process project
        # TODO: order by priority
        for name, Plugin in system.Plugins.items():
            type = Plugin.get_type()
            internal = type == "internal" and name not in self.__config.disable
            external = type == "external" and name in self.__config.enable
            if internal or external:
                Plugin.process_project(self)

        # Connect project
        for document in self.__documents:
            document.project = self

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
    def format(self):
        if self.__format:
            return self.__format
        if self.__document:
            return self.__document.format
        return settings.DEFAULT_FORMAT

    # Build

    def build(self, *, diff=False, print=False):

        # Ensure documents
        if not self.documents:
            raise LivemarkException("No documents to build in the project")

        # Build documents
        outputs = []
        for document in self.documents:
            output = document.build(diff=diff, print=print)
            if output:
                outputs.append(output)
        output = "\n".join(outputs)

        return output
