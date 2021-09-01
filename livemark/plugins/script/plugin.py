import subprocess
from ...plugin import Plugin
from ... import helpers
from ... import errors


class ScriptPlugin(Plugin):
    identity = "script"
    priority = 100

    # Process

    def __init__(self, document):
        super().__init__(document)
        self.__store = []

    def process_document(self, config):
        self.__index = 0

    def process_snippet(self, snippet):

        # Update snippet
        if snippet.type == "script":

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
                        exec(snippet.input, {})
                    output = stdout.getvalue().strip()

                # Missing
                else:
                    message = "Provide a supported script language: bash/python"
                    raise errors.Error(message)

                # General
                output = "\n".join(line.rstrip() for line in output.splitlines())
                cache["lang"] = snippet.lang
                cache["input"] = snippet.input
                cache["output"] = output

            # Apply cache
            self.__index += 1
            snippet.output = cache["output"]
