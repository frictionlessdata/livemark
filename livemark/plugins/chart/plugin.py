import json
import yaml
from ...plugin import Plugin


class ChartPlugin(Plugin):
    identity = "chart"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "chart" and snippet.lang in ["yaml", "json"]:
                if snippet.lang == "yaml":
                    spec = yaml.safe_load(str(snippet.input).strip())
                if snippet.lang == "json":
                    spec = json.loads(str(snippet.input).strip())
                spec = json.dumps(spec, ensure_ascii=False)
                spec = spec.replace("'", "\\'")
                self.__count += 1
                card = snippet.props.get("card")
                elem = f"livemark-chart-{self.__count}"
                if card:
                    elem += "-card"
                chart = {"spec": spec, "elem": elem}
                snippet.output = (
                    self.read_asset("markup.html", card=card, chart=chart) + "\n"
                )

    def process_markup(self, markup):
        if self.__count:
            url = "https://unpkg.com"
            markup.add_script(f"{url}/vega@5.20.2/build/vega.min.js")
            markup.add_script(f"{url}/vega-lite@5.1.0/build/vega-lite.min.js")
            markup.add_script(f"{url}/vega-embed@6.18.2/build/vega-embed.min.js")
