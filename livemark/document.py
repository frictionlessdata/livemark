import yaml
import marko
import subprocess
from jinja2 import Template
from .renderer import LivemarkRenderer
from . import config


class Document:
    def __init__(self, path, *, layout_path=None):
        self.__path = path

    # Process

    def process(self):
        markdown = marko.Markdown(renderer=LivemarkRenderer)

        # Source document
        with open(self.__path) as file:
            source = file.read()
            target = source

        # Preprocess document
        template = Template(target, trim_blocks=True)
        target = template.render()

        # Parse document
        metadata = {}
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)

        # Prepare document
        for code in metadata.get("prepare", []):
            subprocess.run(code, shell=True)

        # Convert document
        target = markdown.convert(target).strip()

        # Cleanup document
        for code in metadata.get("cleanup", []):
            subprocess.run(code, shell=True)

        # Postprocess document
        layout = config.LAYOUT
        if metadata.get("layout"):
            with open(metadata["layout"]) as file:
                layout = file.read()
        template = Template(layout)
        target = template.render(title=metadata.get("title", "Livemark"), content=target)

        return source, target
