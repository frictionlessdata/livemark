import yaml
from .config import Config
from .system import system
from . import settings
from . import helpers
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

    def __init__(self, source, *, update=None, format=None):

        # Infer format
        if not format:
            format = settings.DEFAULT_FORMAT

        # Set attributes
        self.__source = source
        self.__update = update
        self.__format = format
        self.__config = None
        self.__document = None
        self.__documents = []

    def __setattr__(self, name, value):
        if name == "document":
            self.__document = value
        else:  # default setter
            super().__setattr__(name, value)

    @property
    def source(self):
        """Project's source

        Return:
            str: source
        """
        return self.__source

    @property
    def update(self):
        """Project's update

        Return:
            str: update
        """
        return self.__update

    @property
    def format(self):
        """Project's format

        Return:
            str: format
        """
        return self.__format

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

        # Read/process
        self.read()
        self.process()

        # Ensure documents
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

        # Read config
        mapping = yaml.safe_load(helpers.read_file(self.source))
        if self.update:
            mapping.update(self.update)
        self.__config = Config(mapping)

    def process(self):
        """Process the project"""

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
