import os
import re
import sys
import yaml
import deepmerge
import jsonschema
from pathlib import Path
from copy import deepcopy
from frictionless import File
from .system import system
from .exception import LivemarkException
from .helpers import cached_property
from . import settings
from . import helpers


class Document:
    """Livemark document

    API      | Usage
    -------- | --------
    Public   | `from livemark import Document`

    Parameters:
        source (str): path to the document source
        target? (str): path to the document target
        format? (str): format of the document target
        project? (Project): a project to which the document belongs
        create? (bool): whether to create a source if index.md doesn't exist

    """

    def __init__(self, source, *, target=None, format=None, project=None, create=False):

        # Create source
        if create and source == settings.DEFAULT_SOURCE:
            if not os.path.exists(source):
                with open(source, "w"):
                    pass

        # Infer target
        if not target:
            suffix = f".{format or settings.DEFAULT_FORMAT}"
            target = str(Path(source).with_suffix(suffix))

        # Infer format
        if not format:
            file = File(target)
            format = file.format

        # Create plugins
        plugins = []
        for Plugin in system.Plugins:
            plugins.append(Plugin(self))

        # Set attributes
        self.__source = source
        self.__target = target
        self.__format = format
        self.__project = project
        self.__create = create
        self.__plugins = plugins
        self.__preface = None
        self.__content = None
        self.__config = None
        self.__input = None
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
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @property
    def preface(self):
        return self.__preface

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def config(self):
        return self.__config

    @property
    def plugins(self):
        return self.__plugins

    @cached_property
    def title(self):
        prefix = "# "
        for line in self.input.splitlines():
            if line.startswith(prefix):
                return line.lstrip(prefix)

    @cached_property
    def description(self):
        pattern = re.compile(r"^\w")
        for line in self.input.splitlines():
            line = line.strip()
            if pattern.match(line):
                return line

    @cached_property
    def keywords(self):
        return ",".join(self.title.split())

    # Build

    def build(self, *, print=False):
        self.read()
        self.process()
        self.write(print=print)

    # Read

    def read(self):

        # Read input
        with open(self.__source) as file:
            self.__input = file.read()

        # Read preface/content
        self.__preface = ""
        self.__content = self.__input
        if self.__input.startswith("---"):
            parts = self.__input.split("---", maxsplit=2)[1:]
            self.__preface = parts[0].strip()
            self.__content = parts[1].strip()

        # Read config
        self.__config = {}
        if self.__project:
            self.__config = deepcopy(self.__project.config)
        if self.__preface:
            deepmerge.always_merger.merge(self.__config, yaml.safe_load(self.__preface))

        # Process config
        for plugin in self.__plugins:
            self.__config.setdefault(plugin.name, {})
            if not isinstance(self.__config[plugin.name], dict):
                self.__config[plugin.name] = {"self": self.__config[plugin.name]}
            plugin.process_config(self.__config)
            if self.__config[plugin.name] and plugin.profile:
                validator = jsonschema.Draft7Validator(plugin.profile)
                for error in validator.iter_errors(self.__config[plugin.name]):
                    message = f'Invalid "{plugin.name}" config: {error.message}'
                    raise LivemarkException(message)

    # Process

    def process(self):
        if self.__input is None:
            raise LivemarkException("Read document before processing")
        for plugin in self.__plugins:
            plugin.process_document(self)

    # Write

    def write(self, *, print=False):
        if self.__output is None:
            raise LivemarkException("Process document before writing")
        if print:
            sys.stdout.write(self.__output)
            sys.stdout.flush()
            return
        helpers.write_file(self.__target, self.__output)
