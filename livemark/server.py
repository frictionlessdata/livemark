import livereload
from pathlib import Path
from .document import Document
from . import settings


# NOTE:
# We can make this logic more sophisticated by watching
# config changes in livemark.yaml and the main source file
# We also might implement `server.stop` although it's not supported in livereload


class Server:
    def __init__(self, document):
        self.__document = document
        self.__server = livereload.Server()
        self.__config = document.config.copy()

    @property
    def document(self):
        return self.__document

    def start(
        self,
        *,
        host=settings.DEFAULT_HOST,
        port=settings.DEFAULT_PORT,
        file=settings.DEFAULT_FILE,
    ):

        # Create documents
        # TODO: move to document (pages/subdocuments)?
        self.__document.read()
        documents = [self.__document]
        if self.__document.format == "html" and self.__document.config["pages"]:
            for page in self.__document.config["pages"]["items"]:
                page_target = page["path"][1:] or "index.html"
                page_source = str(Path(page_target).with_suffix(".md"))
                if page_source != self.__document.source:
                    page_document = Document(page_source, config=self.__config)
                    documents.append(page_document)

        # Build initially
        for document in documents:
            document.build()

        # Run server
        for document in documents:
            self.__server.watch(document.source, document.build, delay=1)
        self.__server.serve(
            host=host,
            port=port,
            root=".",
            open_url_delay=1,
            default_filename=file,
        )
