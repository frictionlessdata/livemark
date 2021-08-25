from .config import Config
from .document import Document
from .exception import LivemarkException
from . import settings
from . import helpers


class Project:
    def __init__(self, document=None, *, config=None, format=None):
        config = Config(config)
        documents = []

        # Infer format
        if not format:
            format = settings.DEFAULT_FORMAT
            if document:
                format = document.format

        # Add document
        if document:
            documents.append(document)

        # Add documents
        if not documents:
            items = config.get("pages", {}).get("items", [])
            for item in helpers.flatten_items(items, "items"):
                source = helpers.with_format(item["path"], "md")
                target = helpers.with_format(item["path"], format)
                document = Document(source, target=target, name=item["name"])
                documents.append(document)

        # Ensure documents
        if not document:
            raise LivemarkException("No documents found")

        # Set project
        for document in documents:
            document.project = self

        # Set attributes
        self.__config = config
        self.__document = document
        self.__documents = documents

    @property
    def config(self):
        return self.__config

    @property
    def documents(self):
        return self.__documents

    # Build

    def build(self, *, diff=False, print=False):
        outputs = []
        for document in self.documents:
            output = document.build(diff=diff, print=print)
            if output:
                outputs.append(output)
        return "\n".join(outputs)

    # Helpers

    def with_format(self, format):
        document = self.__document.with_format(format)
        return Project(document, config=self.__config, format=format)
