import yaml
import marko
import subprocess
from .renderer import PublixRenderer


class Document:
    def __init__(self, path):
        self.__path = path

    # Process

    def process(self):
        markdown = marko.Markdown(renderer=PublixRenderer)

        # Source document
        with open(self.__path) as file:
            source = file.read()
            target = source

        # Parse document
        prepare = []
        cleanup = []
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)
            if "publix" in metadata:
                prepare.extend(metadata["publix"].get("prepare", []))
                cleanup.extend(metadata["publix"].get("cleanup", []))

        # Prepare document
        for code in prepare:
            subprocess.run(code, shell=True)

        # Convert document
        target = markdown.convert(target)
        target = frontmatter.join(["---"] * 2) + "\n" + target

        # Cleanup document
        for code in cleanup:
            subprocess.run(code, shell=True)

        return source, target
