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
                detector = Detector(field_float_numbers=True)
                with Resource(spec.pop("data", []), detector=detector) as resource:
                    header = resource.header
                    rows = resource.read_rows()
                columns = spec.get("columns", [])
                if not columns:
                    for label in header:
                        columns.append({"data": label})
                width = spec.pop("width", "100%")
                if isinstance(width, int):
                    width = f"{width}px"
                spec.setdefault("columnDefs", [])
                spec["columnDefs"].append(
                    {"targets": "_all", "orderSequence": ["desc", "asc"]}
                )
                spec = json.dumps(spec, ensure_ascii=False)
                spec = spec.replace("'", "\\'")
                self.__count += 1
                card = snippet.props.get("card")
                elem = f"livemark-table-{self.__count}"
                if card:
                    elem += "-card"
                snippet.output = (
                    self.read_asset(
                        "markup.html",
                        card=card,
                        elem=elem,
                        spec=spec,
                        rows=rows,
                        columns=columns,
                        width=width,
                    )
                    + "\n"
                )

    def process_markup(self, markup):
        if self.__count:
            url = "https://cdn.datatables.net/1.11.3"
            markup.add_style(f"{url}/css/jquery.dataTables.css")
            markup.add_script(f"{url}/js/jquery.dataTables.js")
