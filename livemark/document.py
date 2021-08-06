import os
import re
import yaml
import difflib
import deepmerge
import jsonschema
from pathlib import Path
from frictionless import File
from .exception import LivemarkException
from .helpers import cached_property
from .system import system
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
        config? (str|dict): path to a config file or a config dict

    """

    def __init__(self, source, *, target=None, format=None, config=None):

        # Create plugins
        plugins = []
        for Plugin in system.Plugins:
            plugins.append(Plugin(self))

        # Infer target
        if not target:
            suffix = f".{format or settings.DEFAULT_FORMAT}"
            target = str(Path(source).with_suffix(suffix))

        # Infer format
        if not format:
            file = File(target)
            format = file.format

        # Normalize config
        config = config or {}
        if not isinstance(config, dict):
            if os.path.isfile(config):
                with open(config) as file:
                    config = yaml.safe_load(file)

        # Set attributes
        self.__plugins = plugins
        self.__source = source
        self.__target = target
        self.__format = format
        self.__config = config
        self.__preface = None
        self.__content = None
        self.__input = None
        self.__output = None

    @property
    def plugins(self):
        return self.__plugins

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

    def build(self, *, diff=False, print=False):
        self.read()
        self.process()
        written = self.write(diff=diff, print=print)
        return written

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

        # Read/process config
        if self.__preface:
            deepmerge.always_merger.merge(self.__config, yaml.safe_load(self.__preface))
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

    def write(self, *, diff=False, print=False):
        if self.__output is None:
            raise LivemarkException("Process document before writing")

        # Diff
        if diff:
            next = self.output
            prev = helpers.read_file(self.target, default="")
            l1 = prev.splitlines(keepends=True)
            l2 = next.splitlines(keepends=True)
            ld = list(difflib.unified_diff(l1, l2, fromfile="prev", tofile="next"))
            text = ""
            if ld:
                text = "".join(ld)
                helpers.write_stdout(text)
            return text

        # Print
        if print:
            helpers.write_stdout(self.__output)
            return self.__output

        # Save
        helpers.write_file(self.__target, self.__output)
        return self.__output
