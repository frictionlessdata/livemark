from pyquery import PyQuery
from contextlib import contextmanager
from . import helpers
from . import errors


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
        """Markup's input

        Returns:
            str: input
        """
        return self.__input

    @property
    def query(self):
        """Markup's query

        Returns:
            PyQery: query
        """
        return self.__query

    @property
    def output(self):
        """Markup's output

        Returns:
            str?: output
        """
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

    @property
    def plugin(self):
        if not self.__plugin:
            raise errors.Error("Markup is not bound")
        return self.__plugin

    # Bind

    @contextmanager
    def bind(self, plugin):
        """Bind markup to a plugin

        Parameters:
            plugin (Plugin): plugin
        """
        self.__plugin = plugin
        yield self.__plugin
        self.__plugin = None

    # Process

    def process(self, document):
        """Process markup

        Parameters:
            document (Document): document having this markup
        """
        for plugin in document.plugins:
            with self.bind(plugin):
                plugin.process_markup(self)

    # Helpers

    def add_style(self, source, *, target="head", action="append", **context):
        """Add style inside the markup

        Parameters:
            source (str): style path
            target (str): DOM element name
            action (str): DOM action name
            context (dict): template variables
        """
        style = f'<link rel="stylesheet" href="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            style = self.plugin.read_asset(source, **context)
            style = f"<style>\n\n{style}\n\n</style>\n"
        if style not in self.__styles:
            self.__styles.add(style)
            getattr(self.__query(target), action)(style)

    def add_script(self, source, *, target="body", action="append", **context):
        """Add script inside the markup

        Parameters:
            source (str): script path
            target (str): DOM element name
            action (str): DOM action name
            context (dict): template variables
        """
        script = f'<script src="{source}"></script>\n'
        if not helpers.is_remote_path(source):
            script = self.plugin.read_asset(source, **context)
            script = f"<script>\n\n{script}\n\n</script>\n"
        if script not in self.__scripts:
            self.__scripts.add(script)
            getattr(self.__query(target), action)(script)

    def add_markup(self, source, *, target="body", action="append", **context):
        """Add markup inside the markup

        Parameters:
            source (str): markup path
            target (str): DOM element name
            action (str): DOM action name
            context (dict): template variables
        """
        markup = source
        if not source.strip().startswith("<"):
            markup = self.plugin.read_asset(source, **context)
        getattr(self.__query(target), action)(f"\n{markup}\n")
