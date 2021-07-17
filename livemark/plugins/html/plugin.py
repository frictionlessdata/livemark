import os
import marko
import datetime
import jsonschema
import frictionless
from marko.ext.gfm import GFM
from jinja2 import Environment, FileSystemLoader
from .renderer import HtmlRenderer, HtmlExtension
from ..plugin import Plugin
from .. import settings


class MarkdownPlugin(Plugin):
    def process_document(self, document):
        if document.format in ["html"]:
            markdown = marko.Markdown()
            markdown.use(GFM)
            markdown.use(HtmlExtension)
            templating = Environment(
                loader=FileSystemLoader(settings.TEMPLATES),
                trim_blocks=True,
            )

            metadata = document.config
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
            HtmlRenderer.metadata = metadata
            # TODO: finish profile
            # TODO: provide profiles in the features?
            jsonschema.validate(metadata, settings.CONFIG_PROFILE)

            # Preprocess document
            template = templating.from_string(document.input)
            target = template.render(frictionless=frictionless)

            # Convert document
            target = markdown.convert(target).strip()
            metadata["content"] = target

            # TODO: move to the proper place / automate
            metadata["features"] = []
            for name in metadata:
                if name in settings.FEATURES:
                    metadata["features"].append(name)

            # Postprocess document
            layout = settings.LAYOUT
            if metadata.get("layout"):
                with open(metadata["layout"]) as file:
                    layout = file.read()
            template = templating.from_string(layout)
            document.output = template.render(livemark=metadata)
