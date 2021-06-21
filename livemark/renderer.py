import io
import bs4
import sys
import json
import yaml
import marko
import contextlib
import subprocess
from copy import copy
from jinja2 import Template
from marko.ext.gfm import GFM
from marko.inline import RawText
from marko.html_renderer import HTMLRenderer
from frictionless import Resource, Detector
from . import config


class LivemarkRendererMixin(HTMLRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__tables = 0
        self.__charts = 0
        self.__scripts = 0

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
            self.__tables += 1
            self.metadata.setdefault("table", {})
            self.metadata["table"]["count"] = self.__tables
            table = {"spec": spec, "elem": f"livemark-table-{self.__tables}"}
            text = template.render(table=table)
            return text
        if element.lang == "chart":
            spec_yaml = str(element.children[0].children).strip()
            spec_python = yaml.safe_load(spec_yaml)
            spec = json.dumps(spec_python, ensure_ascii=False)
            spec = spec.replace("'", "\\'")
            template = Template(config.CHART)
            self.__charts += 1
            self.metadata.setdefault("chart", {})
            self.metadata["chart"]["count"] = self.__charts
            chart = {"spec": spec, "elem": f"livemark-chart-{self.__charts}"}
            text = template.render(chart=chart)
            return text
        if element.lang == "script":
            code = str(element.children[0].children).strip()
            # TODO: raise on unsupported lang
            lang = "bash" if "bash" in element.extra else "python"
            element.lang = lang
            if not code.startswith("!"):
                with capture() as stdout:
                    # TODO: fix scope
                    exec(code, globals())
                output = stdout.getvalue().strip()
            else:
                try:
                    output = subprocess.check_output(code, shell=True).decode().strip()
                except Exception as exception:
                    output = exception.output.decode().strip()
            output = "\n".join(line.rstrip() for line in output.splitlines())
            text = super().render_fenced_code(element)
            if output:
                target = copy(element)
                target.lang = "markup"
                target.extra = ""
                target.children = [RawText(output)]
                text += "\n"
                text += super().render_fenced_code(target)
            self.__scripts += 1
            self.metadata.setdefault("script", {})
            self.metadata["script"]["count"] = self.__scripts
            return text
        return super().render_fenced_code(element)


class LivemarkExtension:
    renderer_mixins = [LivemarkRendererMixin]


# Internal


@contextlib.contextmanager
def capture(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
