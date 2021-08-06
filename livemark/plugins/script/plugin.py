import subprocess
from ...exception import LivemarkException
from ...plugin import Plugin
from ... import helpers


# TODO: support snippet.mode = 'default' | 'input' | 'output'
class ScriptPlugin(Plugin):
    def process_snippet(self, snippet):

        # Update snippet
        if snippet.type == "script":
            if snippet.lang == "bash":
                try:
                    output = subprocess.check_output(snippet.input, shell=True)
                    output = output.decode().strip()
                except Exception as exception:
                    output = exception.output.decode().strip()
            elif snippet.lang == "python":
                with helpers.capture_stdout() as stdout:
                    exec(snippet.input, {})
                output = stdout.getvalue().strip()
            else:
                message = "Provide a supported script language: bash/python"
                raise LivemarkException(message)
            snippet.output = "\n".join(line.rstrip() for line in output.splitlines())
