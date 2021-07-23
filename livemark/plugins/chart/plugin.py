import json
import yaml
from jinja2 import Template
from ...plugin import Plugin


class ChartPlugin(Plugin):
    def __init__(self):
        self.__count = 0

    def process_snippet(self, snippet):
        if snippet.format == "html":
            if "chart" in snippet.header:
                spec_yaml = str(snippet.input).strip()
                spec_python = yaml.safe_load(spec_yaml)
                spec = json.dumps(spec_python, ensure_ascii=False)
                spec = spec.replace("'", "\\'")
                template = Template(self.read_asset("markup.html"))
                self.__count += 1
                chart = {"spec": spec, "elem": f"livemark-chart-{self.__count}"}
                snippet.output = template.render(chart=chart)