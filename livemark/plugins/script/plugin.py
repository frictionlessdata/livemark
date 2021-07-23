import subprocess
from ...exception import LivemarkException
from ...plugin import Plugin
from ... import helpers


class ScriptPlugin(Plugin):
    def process_snippet(self, snippet):
        if "script" in snippet.header:
            output = ""
            if "bash" in snippet.header:
                try:
                    output = subprocess.check_output(snippet.input, shell=True)
                    output = output.decode().strip()
                except Exception as exception:
                    output = exception.output.decode().strip()
            elif "python" in snippet.header:
                with helpers.capture_stdout() as stdout:
                    # TODO: review globals usage
                    exec(snippet.input, globals())
                output = stdout.getvalue().strip()
            else:
                message = "Provide a supported script language: bash/python"
                raise LivemarkException(message)
            snippet.output = "\n".join(line.rstrip() for line in output.splitlines())
