import yaml
import marko
import subprocess
import frictionless
from jinja2 import Environment, FileSystemLoader
from marko.ext.gfm import GFM
from .renderer import LivemarkExtension
from . import config


class Document:
    def __init__(self, path, *, layout_path=None):
        self.__path = path

    # Process

    def process(self):
        markdown = marko.Markdown()
        markdown.use(GFM)
        markdown.use(LivemarkExtension)
        templating = Environment(
            loader=FileSystemLoader(config.TEMPLATES),
            trim_blocks=True,
        )

        # Source document
        with open(self.__path) as file:
            source = file.read()
            target = source

        # Parse document
        metadata = {}
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)

        # Prepare document
        for code in metadata.get("prepare", []):
            subprocess.run(code, shell=True)

        # Preprocess document
        template = templating.from_string(target)
        target = template.render(frictionless=frictionless)

        # Convert document
        target = markdown.convert(target).strip()

        # Postprocess document
        layout = config.LAYOUT
        if metadata.get("layout"):
            with open(metadata["layout"]) as file:
                layout = file.read()
        template = templating.from_string(layout)
        target = template.render(title=metadata.get("title", "Livemark"), content=target)

        # Cleanup document
        for code in metadata.get("cleanup", []):
            subprocess.run(code, shell=True)

        return source, target
