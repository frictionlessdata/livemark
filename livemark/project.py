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
        config? (str): a path to config file
        format? (str): an output format

    """

    def __init__(self, config=None, format=None):
        self.__format = format or settings.DEFAULT_FORMAT
        self.__config = Config(config)
        self.__document = None
        self.__documents = []

    def __setattr__(self, name, value):
        if name == "document":
            self.__document = value
        else:  # default setter
            super().__setattr__(name, value)

    @property
    def config(self):
        """Project's config

        Return:
            Config: config
        """
        return self.__config

    @property
    def format(self):
        """Project's format

        Return:
            str: format
        """
        return self.__format

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

        # Read documents
        self.read()
        if not self.building_documents:
            raise errors.Error("No documents to build in the project")

        # Build documents
        outputs = []
        for document in self.building_documents:
            output = document.build(diff=diff, print=print)
            if output:
                outputs.append(output)
        output = "\n".join(outputs)

        return output

    # Read

    def read(self):
        """Read the project"""

        # Process project
        for Plugin in system.iterate():
            if Plugin.check_status(self.config):
                Plugin.process_project(self)

        # Read documents
        path = None
        if self.document:
            self.document.read()
            path = self.document.path
        for document in self.documents:
            if document.path != path:
                document.read()

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
