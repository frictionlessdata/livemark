import json
import yaml
from frictionless import Resource, Detector
from ...plugin import Plugin


class TablePlugin(Plugin):
    identity = "table"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "table" and snippet.lang == "yaml":
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
                self.__count += 1
                table = {"spec": spec, "elem": f"livemark-table-{self.__count}"}
                snippet.output = self.read_asset("markup.html", table=table) + "\n"

    def process_markup(self, markup):
        if self.__count:
            url = "https://unpkg.com"
            markup.add_style(f"{url}/handsontable@9.0.0/dist/handsontable.min.css")
            markup.add_script(f"{url}/handsontable@9.0.0/dist/handsontable.min.js")
