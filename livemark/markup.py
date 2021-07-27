from pyquery import PyQuery
from .system import system
from .exception import LivemarkException
from . import helpers


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
        # NOTE:
        # PyQuery uses lxml which esape all the <> inside the tags
        # Here we recover initial formatting for styles and scripts
        # Take into account that this script is fragile (rewrite)
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

    def process(self):
        system.process_markup(self)

    # Bind

    def bind(self, plugin=None):
        if callable(plugin):
            plugin = plugin.__self__
        self.__plugin = plugin
        return self

    @property
    def plugin(self):
        if not self.__plugin:
            raise LivemarkException("The object is not bound to any plugin")
        return self.__plugin

    @property
    def plugin_config(self):
        return self.document.config.get(self.plugin.name, {})

    def add_style(self, source, *, action="append", target="head", **context):
        style = f'<link rel="stylesheet" href="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            style = self.plugin.read_asset(source, **context)
            style = f"<style>\n\n{style}\n\n</style>\n"
        getattr(self.query(target), action)(style)

    def add_script(self, source, *, action="append", target="body", **context):
        script = f'<script src="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            script = self.plugin.read_asset(source, **context)
            script = f"<script>\n\n{script}\n\n</script>\n"
        getattr(self.query(target), action)(script)

    def add_markup(self, source, *, action="append", target="body", **context):
        markup = source
        if not source.strip().startswith("<"):
            markup = self.plugin.read_asset(source, **context)
        getattr(self.query(target), action)(f"\n{markup}\n")
