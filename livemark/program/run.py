import os
import sys
import typer
import marko
import subprocess
from marko import md_renderer
from ..project import Project
from ..snippet import Snippet
from .main import program
from .. import settings
from . import common


# NOTE:
# It's an initial implementation that works directly with markdown renderer
# We need to implement it properly using a normal system flow and TaskPlugin


@program.command(name="run")
def program_run(
    task: str = common.task,
    config: str = common.config,
):
    """Run a Livemark task"""

    try:

        # Handle config
        if not config:
            if os.path.exists(settings.DEFAULT_CONFIG):
                config = settings.DEFAULT_CONFIG

        # Create project
        project = Project(config=config)
        project.read()
        project.process()

        # Extract snippets
        snippets = []
        for document in project.documents:
            document.read()
            markdown = marko.Markdown(renderer=TaskRenderer)
            output = markdown.parse(document.content)
            markdown.renderer.snippets = []
            markdown.render(output)
            snippets.extend(markdown.renderer.snippets)

        # List tasks
        if not task:
            for snippet in snippets:
                typer.secho(snippet.props["id"])
            sys.exit(0)

        # Execute tasks
        scope = {}
        for snippet in snippets:
            if snippet.props["id"].startswith(task):
                if snippet.lang == "bash":
                    subprocess.run(snippet.input, shell=True)
                elif snippet.lang == "python":
                    exec(snippet.input, scope)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)


# Internal


class TaskRenderer(md_renderer.MarkdownRenderer):

    # Render

    def render_fenced_code(self, element):
        input = self.render_children(element).strip()
        header = [element.lang] + element.extra.split()
        snippet = Snippet(input, header=header)
        task_id = snippet.props.get("id")
        if snippet.type == "task" and task_id:
            self.snippets.append(snippet)
        return super().render_fenced_code(element)
