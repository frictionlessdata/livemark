import bs4
import json
import yaml
import marko
from jinja2 import Template
from marko.ext.gfm import GFM
from marko.html_renderer import HTMLRenderer
from frictionless import Resource, Detector
from . import config


class LivemarkRendererMixin(HTMLRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__counter = 0

    # Render

    def render_html_block(self, element):
        markdown = marko.Markdown()
        markdown.use(GFM)
        markdown.use(LivemarkExtension)
        html = bs4.BeautifulSoup(element.children, features="html.parser")
        for node in html.select(".markdown"):
            if len(node.contents) == 1:
                text = node.contents[0]
                if isinstance(text, bs4.element.NavigableString):
                    text = markdown.convert(text)
                    inner = bs4.BeautifulSoup(text, features="html.parser")
                    node.string.replace_with(inner)
        return str(html)

    def render_fenced_code(self, element):
        if element.lang == "table":
            spec_yaml = str(element.children[0].children).strip()
            spec_python = yaml.safe_load(spec_yaml)
            spec_python["licenseKey"] = "non-commercial-and-evaluation"
            detector = Detector(field_float_numbers=True)
            resource = Resource(spec_python.get("data", []), detector=detector)
            header, *lists = resource.to_snap(json=True)
            spec_python["colHeaders"] = header
            spec_python["data"] = lists
            spec = json.dumps(spec_python, ensure_ascii=False)
            spec = spec.replace("'", "\\'")
            template = Template(config.TABLE)
            self.__counter += 1
            text = template.render(spec=spec, elem=f"livemark-{self.__counter}")
            return text
        if element.lang == "chart":
            spec_yaml = str(element.children[0].children).strip()
            spec_python = yaml.safe_load(spec_yaml)
            spec = json.dumps(spec_python, ensure_ascii=False)
            spec = spec.replace("'", "\\'")
            template = Template(config.CHART)
            self.__counter += 1
            text = template.render(spec=spec, elem=f"livemark-{self.__counter}")
            return text
        return super().render_fenced_code(element)


class LivemarkExtension:
    renderer_mixins = [LivemarkRendererMixin]
