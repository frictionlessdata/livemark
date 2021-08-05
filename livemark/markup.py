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
        if callable(plugin):
            plugin = plugin.__self__
        self.__plugin = plugin
        yield self.__plugin
        self.__plugin = None

    # Helpers

    def add_style(self, source, *, action="append", target="head", **context):
        plugin = self.get_plugin()
        style = f'<link rel="stylesheet" href="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            style = plugin.read_asset(source, **context)
            style = f"<style>\n\n{style}\n\n</style>\n"
        if style in self.__styles:
            return
        self.__styles.add(style)
        getattr(self.__query(target), action)(style)

    def add_script(self, source, *, action="append", target="body", **context):
        plugin = self.get_plugin()
        script = f'<script src="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            script = plugin.read_asset(source, **context)
            script = f"<script>\n\n{script}\n\n</script>\n"
        if script in self.__scripts:
            return
        self.__scripts.add(script)
        getattr(self.__query(target), action)(script)

    def add_markup(self, source, *, action="append", target="body", **context):
        markup = source
        plugin = self.get_plugin()
        if not source.strip().startswith("<"):
            markup = plugin.read_asset(source, **context)
        getattr(self.__query(target), action)(f"\n{markup}\n")

    def get_plugin(self):
        if not self.__plugin:
            raise LivemarkException("The object is not bound to any plugin")
        return self.__plugin
