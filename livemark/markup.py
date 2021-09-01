from pyquery import PyQuery
from contextlib import contextmanager
from .exception import LivemarkException
from . import helpers


# NOTE:
# PyQuery uses lxml which esape all the <> inside the tags
# In markup.output we recover initial formatting for styles and scripts
# Take into account that this method is fragile and might need to be rewrited


class Markup:
    """Livemark markup

    API      | Usage
    -------- | --------
    Public   | `from livemark import Markup`

    Parameters:
        input (str): html input for the markup

    """

    def __init__(self, input):
        self.__input = input
        self.__query = PyQuery(input)
        self.__output = None
        self.__plugin = None
        self.__styles = set()
        self.__scripts = set()

    @property
    def input(self):
        return self.__input

    @property
    def query(self):
        return self.__query

    @property
    def output(self):
        lines = []
        is_replacing = False
        output = self.__query.outer_html()
        for line in output.splitlines(keepends=True):
            if line.strip() in ["<style>", "<script>"]:
                is_replacing = True
            elif line.strip() in ["</style>", "</script>"]:
                is_replacing = False
            if is_replacing:
                line = line.replace("&lt;", "<").replace("&gt;", ">")
            lines.append(line)
        output = "".join(lines)
        return output

    # Process

    def process(self, document):
        for plugin in document.plugins:
            with self.bind(plugin):
                plugin.process_markup(self)

    # Bind

    @contextmanager
    def bind(self, plugin=None):
        self.__plugin = plugin
        yield self.__plugin
        self.__plugin = None

    # Helpers

    # TODO: Clean helper methods

    def add_style(self, source, *, target="head", action="append", **context):
        style = f'<link rel="stylesheet" href="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            if not self.__plugin:
                raise LivemarkException("Markup is not bound")
            style = self.__plugin.read_asset(source, **context)
            style = f"<style>\n\n{style}\n\n</style>\n"
        if style in self.__styles:
            return
        self.__styles.add(style)
        getattr(self.__query(target), action)(style)

    def add_script(self, source, *, target="body", action="append", **context):
        script = f'<script src="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            if not self.__plugin:
                raise LivemarkException("Markup is not bound")
            script = self.__plugin.read_asset(source, **context)
            script = f"<script>\n\n{script}\n\n</script>\n"
        if script in self.__scripts:
            return
        self.__scripts.add(script)
        getattr(self.__query(target), action)(script)

    def add_markup(self, source, *, target="body", action="append", **context):
        markup = source
        if not source.strip().startswith("<"):
            if not self.__plugin:
                raise LivemarkException("Markup is not bound")
            markup = self.__plugin.read_asset(source, **context)
        getattr(self.__query(target), action)(f"\n{markup}\n")
