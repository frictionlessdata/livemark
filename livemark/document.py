import yaml
import marko
import subprocess
from jinja2 import Template
from .renderer import LivemarkRenderer
from . import config


class Document:
    def __init__(self, path, *, layout_path=None):
        self.__path = path
        self.__layout = config.LAYOUT
        if layout_path:
            with open(layout_path) as file:
                self.__layout = file.read()

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
        prepare = []
        cleanup = []
        frontmatter = None
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)
            if "livemark" in metadata:
                prepare.extend(metadata["livemark"].get("prepare", []))
                cleanup.extend(metadata["livemark"].get("cleanup", []))

        # Prepare document
        for code in prepare:
            subprocess.run(code, shell=True)

        # Convert document
        target = markdown.convert(target).strip()
        if frontmatter:
            target = frontmatter.join(["---"] * 2) + "\n" + target

        # Cleanup document
        for code in cleanup:
            subprocess.run(code, shell=True)

        # Postprocess document
        template = Template(self.__layout)
        target = template.render(content=target)

        return source, target
