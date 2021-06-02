import bs4
import json
import yaml
import marko
from jinja2 import Template
from marko.ext.gfm import GFM
from marko.html_renderer import HTMLRenderer
from . import config


class LivemarkRendererMixin(HTMLRenderer):

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
        if "table" in element.lang or "table" in element.extra:
            path = str(element.children[0].children).strip()
            template = Template(config.TABLE)
            text = template.render(path=path, id="table-example")
            return text
        if "chart" in element.lang or "chart" in element.extra:
            spec_yaml = str(element.children[0].children).strip()
            spec_python = yaml.safe_load(spec_yaml)
            spec = json.dumps(spec_python)
            template = Template(config.CHART)
            text = template.render(spec=spec, id="chart-example")
            return text
        return super().render_fenced_code(element)


class LivemarkExtension:
    renderer_mixins = [LivemarkRendererMixin]
