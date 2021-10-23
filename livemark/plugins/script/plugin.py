import subprocess
from ...plugin import Plugin
from ... import helpers


# NOTE:
# Consider making the scope publicly available so other plugins
# would be able to use it. For example, creating a table/chart/etc from a var


class ScriptPlugin(Plugin):
    identity = "script"
    priority = 60

    # Process

    def __init__(self, document):
        super().__init__(document)
        self.__store = []
        self.__scope = {}

    def process_document(self, config):
        self.__index = 0

    def process_snippet(self, snippet):
        if snippet.type == "script" and snippet.lang in ["python", "bash"]:

            # Acquire cache
            cache = helpers.list_setdefault(
                self.__store,
                self.__index,
                default={},
            )

            # Invalidate cache
            if cache:
                hit = cache["lang"] == snippet.lang and cache["input"] == snippet.input
                if not hit:
                    cache = {}
                    self.__store = self.__store[: self.__index]
                    self.__store.append(cache)

            # Populate cache
            if not cache:

                # Bash
                if snippet.lang == "bash":
                    try:
                        output = subprocess.check_output(snippet.input, shell=True)
                        output = output.decode().strip()
                    except Exception as exception:
                        output = exception.output.decode().strip()

                # Python
                elif snippet.lang == "python":
                    with helpers.capture_stdout() as stdout:
                        exec(snippet.input, self.__scope)
                    output = stdout.getvalue().strip()

                # General
                output = "\n".join(line.rstrip() for line in output.splitlines())
                cache["lang"] = snippet.lang
                cache["input"] = snippet.input
                cache["output"] = output

            # Apply cache
            self.__index += 1
            snippet.output = cache["output"]
