import sys
import typer
from pathlib import Path
from livereload import Server
from ..document import Document
from .main import program
from . import common


# NOTE:
# We can make this logic more sophisticated by watching
# config changes in livemark.yaml and the main source file


@program.command(name="start")
def program_start(
    source: str = common.source,
    target: str = common.target,
    format: str = common.format,
    config: str = common.config,
):
    """Start a Livemark server."""

    try:

        # Create document
        document = Document(
            source,
            target=target,
            format=format,
            config=config,
            create=True,
        )

        # Create documents
        document.read()
        documents = [document]
        for page in document.config["pages"]["items"]:
            page_target = page["path"][1:] or "index.html"
            page_source = str(Path(page_target).with_suffix(".md"))
            if page_source != source:
                page_document = Document(page_source, project=document.project)
                documents.append(page_document)

        # Build initially
        for document in documents:
            document.build()

        # Run server
        server = Server()
        for document in documents:
            server.watch(document.source, document.build, delay=1)
        server.serve(host="localhost", port=7000, root=".", open_url_delay=1)

    except Exception as exception:
        typer.secho(str(exception), err=True, fg=typer.colors.RED, bold=True)
        sys.exit(1)
