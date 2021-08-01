import subprocess
from ...exception import LivemarkException
from ...plugin import Plugin
from ... import helpers


class ScriptPlugin(Plugin):
    def process_snippet(self, snippet):

        # Update snippet
        if snippet.modifier == "script":
            if snippet.language == "bash":
                try:
                    output = subprocess.check_output(snippet.input, shell=True)
                    output = output.decode().strip()
                except Exception as exception:
                    output = exception.output.decode().strip()
            elif snippet.language == "python":
                with helpers.capture_stdout() as stdout:
                    exec(snippet.input, {})
                output = stdout.getvalue().strip()
            else:
                message = "Provide a supported script language: bash/python"
                raise LivemarkException(message)
            snippet.output = "\n".join(line.rstrip() for line in output.splitlines())
