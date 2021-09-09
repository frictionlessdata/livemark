from .document import Document
from .config import Config
from .system import system
from . import settings
from . import errors


class Project:
    """Livemark project

    Parameters:
        source (str): path to the document source
        target? (str): path to the document target
        format? (str): an output format
        config? (str): a path to config file

    """

    def __init__(
        self,
        source=None,
        *,
        target=None,
        format=None,
        config=None,
    ):

        # Create document
        document = None
        if source:
            document = Document(source, target=target, format=format, project=self)

        # Infer format
        if not format:
            format = document.format if document else settings.DEFAULT_FORMAT

        # Set attributes
        self.__documents = []
        self.__config_source = config
        self.__document = document
        self.__format = format
        self.__config = None

    @property
    def document(self):
        """Project's document

        Return:
            Document?: document
        """
        return self.__document

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

    @property
    def building_sources(self):
        """Project's building sources

        Return:
            str[]: sources
        """
        sources = []
        if self.config and self.config.source:
            sources.append(self.config.source)
        return sources

    # Build

    def build(self, *, diff=False, print=False):
        """Build the project

        Parameters:
            diff (bool): print the diff
            print (bool): print the result

        Returns:
            str: concatenated documents output
        """

        # Read/process
        self.read()
        self.process()

        # Ensure documents
        if not self.building_documents:
            raise errors.Error("No documents to build in the project")

        # Read documents
        for document in self.documents:
            document.read()

        # Build documents
        outputs = []
        for document in self.building_documents:
            output = document.build(diff=diff, print=print)
            if output:
                outputs.append(output)
        output = "\n".join(outputs)

        # Return output
        return output

    # Read

    def read(self):
        """Read the project"""
        self.__config = Config(self.__config_source)

    def process(self):
        """Process the project"""

        # Ensure read
        if self.config is None:
            raise errors.Error("Read project before processing")

        # Process project
        for Plugin in system.iterate():
            if Plugin.check_status(self.config):
                Plugin.process_project(self)

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
