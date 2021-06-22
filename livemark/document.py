import os
import yaml
import marko
import deepmerge
import subprocess
import jsonschema
import frictionless
from datetime import datetime
from marko.ext.gfm import GFM
from jinja2 import Environment, FileSystemLoader
from .renderer import LivemarkExtension, LivemarkRendererMixin
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
        if os.path.isfile("livemark.yaml"):
            with open("livemark.yaml") as file:
                metadata = deepmerge.always_merger.merge(metadata, yaml.safe_load(file))
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = deepmerge.always_merger.merge(
                metadata, yaml.safe_load(frontmatter)
            )
            # TODO: find a better place for it
            metadata.setdefault("title", "Livemark")
            metadata.setdefault("time", {})
            metadata["time"]["current"] = datetime.fromtimestamp(
                os.path.getmtime(self.__path)
            )
            # TODO: set these in the renderer
            metadata["markup"] = True
            # TODO: it's a hack as marko doesn't have context
            LivemarkRendererMixin.metadata = metadata
        # TODO: finish profile
        # TODO: provide profiles in the features?
        jsonschema.validate(metadata, config.CONFIG_PROFILE)

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
        livemark = metadata.copy()
        livemark["document"] = target
        target = template.render(livemark=livemark)

        # Cleanup document
        for code in metadata.get("cleanup", []):
            subprocess.run(code, shell=True)

        return source, target
