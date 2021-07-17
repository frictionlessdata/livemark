import os
import yaml
from .project import Project
from . import settings


class Document:
    def __init__(self, path=None, *, project=None):
        path = path or settings.DOCUMENT_PATH
        project = project or Project()

        # Create document
        if path == "index.md":
            if not os.path.exists(path):
                with open(path, "w") as file:
                    pass

        # Read source
        with open(path) as file:
            source = file.read()

        # Read config
        config = project.config.clone()
        if source.startswith("---"):
            frontmatter, source = source.split("---", maxsplit=2)[1:]
            config.merge(yaml.safe_load(frontmatter))

        # Save attributes
        self.__path = path
        self.__project = project
        self.__config = config
        self.__source = source
        self.__target = ""

    @property
    def path(self):
        return self.__path

    @property
    def project(self):
        return self.__project

    @property
    def config(self):
        return self.__config

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    # Process

    def process(self):
        pass
