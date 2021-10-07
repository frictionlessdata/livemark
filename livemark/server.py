import livereload
from . import settings


# NOTE:
# Consider implementing `server.stop` although it's not supported in livereload


class Server:
    """Livemark server

    Parameters:
        proejct (Project): a project to server

    """

    def __init__(self, project):
        self.__project = project
        self.__server = livereload.Server()

    @property
    def project(self):
        """Server's project

        Return:
            Project: project
        """
        return self.__project

    # Start

    def start(
        self,
        *,
        host=settings.DEFAULT_HOST,
        port=settings.DEFAULT_PORT,
        file=settings.DEFAULT_FILE,
    ):
        """Start the server

        Parameters:
            host (str): HTTP host
            port (int): HTTP port
            file (str): index file path
        """

        # Build documents
        self.project.build()
        for source in self.project.building_sources:
            self.__server.watch(source, self.project.build, delay=1)
        for document in self.project.building_documents:
            self.__server.watch(document.source, document.build, delay=1)

        # Run server
        self.__server.serve(
            host=host,
            port=port,
            root=".",
            open_url_delay=1,
            default_filename=file,
        )
