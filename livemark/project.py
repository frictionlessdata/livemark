from pathlib import Path
from .config import Config
from .helpers import cached_property
from .document import Document
from . import helpers


class Project:
    def __init__(self, *, config=None):
        self.__config = Config(config)

    @cached_property
    def config(self):
        return self.__config

    @cached_property
    def documents(self):
        documents = []
        items = self.config.get("pages", {}).get("items", [])
        for item in helpers.flatten_items(items, "items"):
            source = str(Path(item["path"]).with_suffix(".md"))
            document = Document(source, project=self)
            documents.append(document)
        return documents
