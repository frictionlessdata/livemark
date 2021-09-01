from .config import Config
from .system import system
from . import settings
from . import errors


# NOTE:
# Review whether it's right to read all the documents on init (duplicate with document?)
# We read them to get access to configs and iferred data


class Project:
    """Livemark project

    API      | Usage
    -------- | --------
    Public   | `from livemark import Project`

    Parameters:
        document (Document): a document to build
        config? (str): a path to config file
        format? (str): an output format

    """

    def __init__(self, document=None, *, config=None, format=None):
        self.__documents = [document] if document else []
        self.__config = Config(config)
        self.__document = document
        self.__format = format
        self.__context = {}

        # Process project
        for Plugin in system.iterate():
            if Plugin.check_status(self.__config):
                Plugin.process_project(self)

        # Read documents
        for document in self.__documents:
            document.project = self
            document.read()

    @property
    def format(self):
        """Project's format

        Return:
            str: format
        """
        if self.__format:
            return self.__format
        if self.__document:
            return self.__document.format
        return settings.DEFAULT_FORMAT

    @property
    def config(self):
        """Project's config

        Return:
            Config: config
        """
        return self.__config

    @property
    def document(self):
        """Project's document

        Return:
            Document?: document
        """
        return self.__document

    @property
    def documents(self):
        """Project's documents

        Return:
            Document[]: documents
        """
        return self.__documents

    @property
    def building_documents(self):
        """Project's building documents

        Return:
            Document[]: documents
        """
        return [self.document] if self.document else self.documents

    # Build

    def build(self, *, diff=False, print=False):
        """Build the project

        Parameters:
            diff (bool): print the diff
            print (bool): print the result

        Returns:
            str: concatenated documents output
        """

        # Ensure documents
        if not self.documents:
            raise errors.Error("No documents to build in the project")

        # Build documents
        outputs = []
        for document in self.building_documents:
            output = document.build(diff=diff, print=print)
            if output:
                outputs.append(output)
        output = "\n".join(outputs)

        return output

    # Helpers

    def get_document(self, path):
        """Return document

        Parameters:
            path (str): document's path

        Return:
            Document?: document if found
        """
        for document in self.documents:
            if document.path == path:
                return document
