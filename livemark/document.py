import yaml
import subprocess
from frictionless import File
from .system import system
from .project import Project
from .helpers import cached_property
from . import settings


class Document:
    def __init__(self, source=None, *, target=None, project=None):
        # TODO: review whether it needs to default
        source = source or settings.DEFAULT_PATH
        target = target or settings.DEFAULT_TARGET
        project = project or Project()

        # Read input
        with open(source) as file:
            input = file.read()

        # Read preface
        preface = ""
        if input.startswith("---"):
            preface, input = input.split("---", maxsplit=2)[1:]

        # Read config
        config = project.config.clone()
        if preface:
            config.merge(yaml.safe_load(preface))

        # Save attributes
        self.__source = source
        self.__target = target
        self.__project = project
        self.__preface = preface
        self.__config = config
        self.__input = input
        self.__output = None

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @cached_property
    def format(self):
        file = File(self.target)
        return file.format

    @property
    def project(self):
        return self.__project

    @property
    def preface(self):
        return self.__preface

    @property
    def config(self):
        return self.__config

    @property
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    # Process

    def prepare(self):
        for code in self.config.get("prepare", []):
            subprocess.run(code, shell=True)

    def process(self):
        return system.process_document(self)

    def cleanup(self):
        for code in self.config.get("cleanup", []):
            subprocess.run(code, shell=True)
