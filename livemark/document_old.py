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
from .markdown import LivemarkMarkdownRenderer
from .metadata import Metadata
from . import config


class Document:
    def __init__(self, path, *, layout_path=None):
        self.__path = path

    # Process

    def process_html(self):
        markdown = marko.Markdown()
        markdown.use(GFM)
        markdown.use(LivemarkExtension)
        templating = Environment(
            loader=FileSystemLoader(config.TEMPLATES),
            trim_blocks=True,
        )

        # Create document
        if self.__path == "index.md":
            if not os.path.exists(self.__path):
                with open(self.__path, "w") as file:
                    pass

        # Source document
        with open(self.__path) as file:
            source = file.read()
            target = source

        # Parse document
        metadata = Metadata()
        if os.path.isfile("livemark.yaml"):
            with open("livemark.yaml") as file:
                metadata = deepmerge.always_merger.merge(metadata, yaml.safe_load(file))
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = deepmerge.always_merger.merge(
                metadata, yaml.safe_load(frontmatter)
            )

        # TODO: find a better place for it
        metadata["path"] = "/" + (
            self.__path.replace(".md", ".html") if self.__path != "index.md" else ""
        )
        metadata.setdefault("title", "Livemark")
        metadata.setdefault("time", {})
        if metadata["time"] is True:
            metadata["time"] = {}
        metadata["time"]["current"] = datetime.fromtimestamp(
            os.path.getmtime(self.__path)
        )
        # TODO: it's a quick hack
        if metadata.get("pages"):
            current = None
            for number, link in enumerate(metadata["pages"]["links"], start=1):
                if link["path"] == metadata["path"]:
                    current = number
            if current > 1:
                metadata["prev"] = metadata["pages"]["links"][current - 2]
            if current < len(metadata["pages"]["links"]):
                metadata["next"] = metadata["pages"]["links"][current]
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
        metadata["content"] = target

        # TODO: move to the proper place / automate
        metadata["features"] = []
        for name in metadata:
            if name in config.FEATURES:
                metadata["features"].append(name)

        # Postprocess document
        layout = config.LAYOUT
        if metadata.get("layout"):
            with open(metadata["layout"]) as file:
                layout = file.read()
        template = templating.from_string(layout)
        target = template.render(livemark=metadata)

        # Cleanup document
        for code in metadata.get("cleanup", []):
            subprocess.run(code, shell=True)

        return source, target

    def process_markdown(self):
        markdown = marko.Markdown(renderer=LivemarkMarkdownRenderer)

        # Source document
        with open(self.__path) as file:
            source = file.read()
            target = source

        # Parse document
        metadata = Metadata()
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)

        # Prepare document
        for code in metadata.get("prepare", []):
            subprocess.run(code, shell=True)

        # Convert document
        target = markdown.convert(target)
        if frontmatter:
            target = frontmatter.join(["---"] * 2) + "\n" + target

        # Cleanup document
        for code in metadata.get("cleanup", []):
            subprocess.run(code, shell=True)

        return source, target
