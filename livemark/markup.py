import os
import inspect
from jinja2 import Template
from pyquery import PyQuery
from .system import system
from .exception import LivemarkException


class Markup:
    def __init__(self, input, *, document):
        self.__input = input
        self.__query = PyQuery(input)
        self.__document = document
        self.__output = ""
        self.__plugin = None

    def __enter__(self):
        assert self.plugin
        return self

    def __exit__(self, type, value, traceback):
        self.bind()

    @property
    def input(self):
        return self.__input

    @property
    def query(self):
        return self.__query

    @property
    def document(self):
        return self.__document

    @property
    def output(self):
        # PyQuery uses lxml which esape all the <> inside the tags
        # Here we recover initial formatting for styles and scripts
        lines = []
        is_replacing = False
        output = self.__query.html()
        for line in output.splitlines(keepends=True):
            if line.strip() in ["<style>", "<script>"]:
                is_replacing = True
            elif line.strip() in ["</style>", "</script>"]:
                is_replacing = False
            if is_replacing:
                line = line.replace("&lt;", "<").replace("&gt;", ">")
            lines.append(line)
        return "".join(lines)

    def process(self):
        system.process_markup(self)

    # Helpers

    def bind(self, plugin=None):
        if callable(plugin):
            plugin = plugin.__self__
        self.__plugin = plugin
        return self

    @property
    def plugin(self):
        if not self.__plugin:
            raise LivemarkException("The markup is not bound to any plugin")
        return self.__plugin

    @property
    def plugin_config(self):
        return self.document.config.get(self.plugin.name, {})

    def add_style(self, path, *, target="head", **context):
        style = self.read_asset(path, tag="style", **context)
        self.query(target).append(f"\n<style>\n\n{style}\n\n</style>\n")

    def add_script(self, path, *, target="body", **context):
        script = self.read_asset(path, tag="script", **context)
        self.query(target).append(f"\n<script>\n\n{script}\n\n</script>\n")

    def add_markup(self, path, *, target="body", **context):
        element = self.read_asset(path, **context)
        self.query(target).append(f"\n{element}\n")

    def read_asset(self, *path, **context):
        dir = os.path.dirname(inspect.getfile(self.plugin.__class__))
        path = os.path.join(dir, *path)
        with open(path) as file:
            text = file.read()
        if context:
            template = Template(text)
            text = template.render(**context)
        return text
