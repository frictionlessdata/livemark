import json
import yaml
from jinja2 import Template
from frictionless import Resource, Detector
from ...plugin import Plugin


class TablePlugin(Plugin):
    def process_config(self, config):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format != "html":
            return

        # Update snippet
        if snippet.type == "table":
            if snippet.lang == "yaml":
                spec_yaml = str(snippet.input).strip()
                spec_python = yaml.safe_load(spec_yaml)
                spec_python["licenseKey"] = "non-commercial-and-evaluation"
                detector = Detector(field_float_numbers=True)
                resource = Resource(spec_python.get("data", []), detector=detector)
                header, *lists = resource.to_snap(json=True)
                spec_python["colHeaders"] = header
                spec_python["data"] = lists
                spec = json.dumps(spec_python, ensure_ascii=False)
                spec = spec.replace("'", "\\'")
                template = Template(self.read_asset("markup.html"))
                self.__count += 1
                table = {"spec": spec, "elem": f"livemark-table-{self.__count}"}
                snippet.output = template.render(table=table) + "\n"

    def process_markup(self, markup):
        markup.add_style("https://unpkg.com/handsontable@9.0.0/dist/handsontable.min.css")
        markup.add_script("https://unpkg.com/handsontable@9.0.0/dist/handsontable.min.js")
