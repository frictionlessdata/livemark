import livereload
from . import settings


# NOTE:
# We can make this logic more sophisticated by watching
# config changes in livemark.yaml and the main source file
# We also might implement `server.stop` although it's not supported in livereload


class Server:
    def __init__(self, document):
        self.__document = document
        self.__server = livereload.Server()

    @property
    def document(self):
        return self.__document

    # Start

    def start(
        self,
        *,
        host=settings.DEFAULT_HOST,
        port=settings.DEFAULT_PORT,
        file=settings.DEFAULT_FILE,
    ):

        # Build initially
        for document in self.document.project.documents:
            document.build()

        # Run server
        for document in self.document.project.documents:
            self.__server.watch(document.source, document.build, delay=1)
        self.__server.serve(
            host=host,
            port=port,
            root=".",
            open_url_delay=1,
            default_filename=file,
        )
