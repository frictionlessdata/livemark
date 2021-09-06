import os
from ...plugin import Plugin
from ...document import Document
from ... import helpers


# TODO:
# Move internal script to the plugin from 404.md (sync with blog)?
# Can we make server show 404.html also locally (livereload)?
# Remove 404 from the pages list


class RedirectPlugin(Plugin):
    identity = "redirect"
    validity = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["prev", "next"],
                    "properties": {
                        "prev": {"type": "string"},
                        "next": {"type": "string"},
                    },
                },
            },
        },
    }

    # Context

    @property
    def items(self):
        return self.config.get("items", [])

    # Process

    @staticmethod
    def process_project(project):
        items = project.config.get("redirect", {}).get("items", [])
        if items:
            missing_default = os.path.join(os.path.dirname(__file__), "missing.md")
            missing_source = "404.md"
            if not os.path.isfile(missing_source):
                helpers.copy_file(missing_default, missing_source)
            project.documents.append(Document(missing_source, project=project))
