import os
import inspect
from jinja2 import Template


# NOTE:
# Consider cached Plugin.document/project_property if optimization is needed


class Plugin:
    """Livemark plugin

    API      | Usage
    -------- | --------
    Public   | `from livemark import Plugin`

    Parameters:
        document (Document): a document to which the plulgin belongs

    """

    identity = ""
    """Plugin's name
    """

    priority = 0
    """Plugin's processing priority
    """

    validity = {}
    """Plugin's JSON Schema for config validation
    """

    def __init__(self, document):
        self.__document = document

    @property
    def config(self):
        """Plugin's config (empty if not provided)

        Returns:
          dict: config
        """
        return self.__document.config.get(self.identity, {})

    @property
    def document(self):
        """Plugin's document it belongs to

        Returns:
          Document: document
        """
        return self.__document

    # Process

    @staticmethod
    def process_project(project):
        """Process project

        Parameters:
          project (Project): a project to process
        """
        pass

    def process_document(self, document):
        """Process document

        Parameters:
          document (Markup): a document to process
        """
        pass

    def process_snippet(self, snippet):
        """Process snippet

        Parameters:
          snippet (Markup): a snippet to process
        """
        pass

    def process_markup(self, markup):
        """Process markup

        Parameters:
          markup (Markup): a markup to process
        """
        pass

    # Helpers

    def read_asset(self, *path, **context):
        """Read plugin's asset

        Parameters:
          path (str[]): paths to join
          context (dict): template variables

        Returns:
            str: a read asset
        """
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        context["plugin"] = self
        with open(path) as file:
            template = Template(file.read().strip(), trim_blocks=True)
            text = template.render(**context)
        return text

    @classmethod
    def check_status(cls, config):
        """Check whether the plugin is active in given config

        Parameters:
          config (Config): a config

        Returns:
          bool: whether active
        """
        type = "external" if cls.__module__.startswith("livemark_") else "internal"
        internal = type == "internal" and config.status.get(cls.identity) is not False
        external = type == "external" and config.status.get(cls.identity) is True
        return internal or external
