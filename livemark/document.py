import re
import yaml
import difflib
from pathlib import Path
from frictionless import File
from .exception import LivemarkException
from .config import Config
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
        project? (Project): a project object of the document

    """

    def __init__(self, source, *, target=None, format=None, project=None):

        # Infer target
        if not target:
            suffix = f".{format or settings.DEFAULT_FORMAT}"
            target = str(Path(source).with_suffix(suffix))

        # Infer format
        if not format:
            file = File(target)
            format = file.format

        # Set attributes
        self.__source = source
        self.__target = target
        self.__format = format
        self.__project = project
        self.__plugins = None
        self.__config = None
        self.__preface = None
        self.__content = None
        self.__input = None
        self.__output = None

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @property
    def format(self):
        return self.__format

    @property
    def project(self):
        return self.__project

    @property
    def plugins(self):
        return self.__plugins

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
    def name(self):
        return self.title

    @property
    def path(self):
        return str(Path(self.source).with_suffix(""))

    @property
    def title(self):
        prefix = "# "
        for line in self.input.splitlines():
            if line.startswith(prefix):
                return line.lstrip(prefix)

    @property
    def description(self):
        pattern = re.compile(r"^\w")
        for line in self.input.splitlines():
            line = line.strip()
            if pattern.match(line):
                return line

    @property
    def keywords(self):
        return ",".join(map(str.lower, self.title.split()))

    # Build

    def build(self, *, diff=False, print=False):
        self.read()
        self.process()
        output = self.write(diff=diff, print=print)
        return output

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
        self.__config = Config({})
        if self.__project:
            self.__config = self.__project.config.to_copy()
        if self.__preface:
            self.__config = self.__config.to_merge(yaml.safe_load(self.__preface))

        # Create plugins
        if self.__plugins is None:
            self.__plugins = []
            for Plugin in system.builtin + system.internal:
                if Plugin.get_name() not in self.__config.disable:
                    self.__plugins.append(Plugin(self))
            for Plugin in system.external:
                if Plugin.get_name() in self.__config.enable:
                    self.__plugins.append(Plugin(self))
            self.__plugins = helpers.order_objects(self.__plugins, "priority")

    # Process

    def process(self):
        if self.__content is None:
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

    # Helpers

    def get_plugin(self, name):
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
