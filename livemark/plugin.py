import os
import inspect
from jinja2 import Template
from .helpers import cached_property


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

    # Actions

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
        project = self.document.project
        dir = os.path.dirname(inspect.getfile(self.__class__))
        path = os.path.join(dir, *path)
        context.update(project.context)
        context["plugin"] = self
        with open(path) as file:
            template = Template(file.read().strip(), trim_blocks=True)
            text = template.render(**context)
        return text

    @classmethod
    def check_active(cls, config):
        """Check whether the plugin is active in given config

        Parameters:
          config (Config): a config

        Returns:
          bool: whether active
        """
        type = "external" if cls.__module__.startswith("livemark_") else "internal"
        internal = type == "internal" and cls.identity not in config.disabled
        external = type == "external" and cls.identity in config.enabled
        return internal or external

    # TODO: review whether we need it (add cache arg or use property/cached_property?)
    property = cached_property
