import re
import yaml
import difflib
from frictionless import File
from .config import Config
from .system import system
from . import settings
from . import helpers
from . import errors


# TODO: make document required or initialize it


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

    def __init__(self, source, *, target=None, format=None):

        # Infer target
        if not target:
            format = format or settings.DEFAULT_FORMAT
            target = helpers.with_format(source, format)

        # Infer format
        if not format:
            file = File(target)
            format = file.format

        # Set attributes
        self.__source = source
        self.__target = target
        self.__format = format
        self.__project = None
        self.__plugins = None
        self.__config = None
        self.__preface = None
        self.__content = None
        self.__input = None
        self.__output = None

    def __setattr__(self, name, value):
        if name == "project":
            self.__project = value
        elif name == "output":
            self.__output = value
        elif name == "content":
            self.__content = value
        else:  # default setter
            super().__setattr__(name, value)

    @property
    def source(self):
        """Document's source

        Returns:
            str: source
        """
        return self.__source

    @property
    def target(self):
        """Document's target

        Returns:
            str: target
        """
        return self.__target

    @property
    def format(self):
        """Document's format

        Returns:
            str: format
        """
        return self.__format

    @property
    def project(self):
        """Document's project

        Returns:
            Project: project
        """
        return self.__project

    @property
    def plugins(self):
        """Document's plugins

        Returns:
            Plugin[]?: plugins
        """
        return self.__plugins

    @property
    def input(self):
        """Document's input

        Returns:
            str?: input
        """
        return self.__input

    @property
    def output(self):
        """Document's output

        Returns:
            str?: output
        """
        return self.__output

    @property
    def preface(self):
        """Document's preface

        Returns:
            str?: preface
        """
        return self.__preface

    @property
    def content(self):
        """Document's content

        Returns:
            str?: content
        """
        return self.__content

    @property
    def config(self):
        """Document's config

        Returns:
            Config?: config
        """
        return self.__config

    @property
    def name(self):
        """Document's name

        Returns:
            str: name
        """
        return self.title or self.path

    @property
    def path(self):
        """Document's path

        Returns:
            str: path
        """
        return helpers.with_format(self.source, "")

    @property
    def title(self):
        """Document's title

        Returns:
            str?: title
        """
        if self.content:
            prefix = "# "
            for line in self.content.splitlines():
                if line.startswith(prefix):
                    return line.lstrip(prefix)

    @property
    def description(self):
        """Document's description

        Returns:
            str?: description
        """
        if self.content:
            pattern = re.compile(r"^\w")
            for line in self.content.splitlines():
                line = line.strip()
                if pattern.match(line):
                    return line

    @property
    def keywords(self):
        """Document's keywords

        Returns:
            str?: keywords
        """
        if self.content:
            return ",".join(map(str.lower, self.title.split()))

    # Build

    def build(self, *, diff=False, print=False):
        """Build the document

        Parameters:
            diff (bool): print the diff
            print (bool): print the result

        Returns:
            str: output
        """
        self.read()
        self.process()
        output = self.write(diff=diff, print=print)
        return output

    # Read

    def read(self):
        """Read the document"""

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
            for Plugin in system.iterate():
                if Plugin.check_status(self.__config):
                    self.__plugins.append(Plugin(self))

    # Process

    def process(self):
        """Process the document"""

        # Ensure read
        if self.__content is None:
            raise errors.Error("Read document before processing")

        # Iterate plugins
        for plugin in self.__plugins:
            plugin.process_document(self)

    # Write

    def write(self, *, diff=False, print=False):
        """Write the document

        Parameters:
            diff (bool): print the diff
            print (bool): print the result

        Returns:
            str: output
        """

        # Ensure processed
        if self.__output is None:
            raise errors.Error("Process document before writing")

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
        """Get document's plugin by name

        Parameters:
            name (str): plugin name
        """
        for plugin in self.plugins:
            if plugin.identity == name:
                return plugin
