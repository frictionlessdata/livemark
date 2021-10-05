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
            if snippet.type == "table" and snippet.lang in ["yaml", "json"]:
                if snippet.lang == "yaml":
                    spec = yaml.safe_load(str(snippet.input).strip())
                if snippet.lang == "json":
                    spec = json.loads(str(snippet.input).strip())
                spec["licenseKey"] = "non-commercial-and-evaluation"
                detector = Detector(field_float_numbers=True)
                with Resource(spec.get("data", []), detector=detector) as resource:
                    # TODO: export as a dict not list?
                    header, *lists = resource.to_snap(json=True)
                spec.setdefault("colHeaders", header)
                spec["data"] = lists
                spec = json.dumps(spec, ensure_ascii=False)
                spec = spec.replace("'", "\\'")
                self.__count += 1
                # TODO: move to document? find a better way?
                card = snippet.props.get("card")
                elem = f"livemark-table-{self.__count}"
                if card:
                    elem += "-card"
                table = {"spec": spec, "elem": elem}
                snippet.output = (
                    self.read_asset("markup.html", card=card, table=table) + "\n"
                )

    def process_markup(self, markup):
        if self.__count:
            url = "https://unpkg.com"
            markup.add_style(f"{url}/handsontable@10.0.0/dist/handsontable.min.css")
            markup.add_script(f"{url}/handsontable@10.0.0/dist/handsontable.min.js")
