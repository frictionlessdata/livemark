import json
import yaml
from ...plugin import Plugin
from ... import helpers


class MapPlugin(Plugin):
    identity = "map"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "map" and snippet.lang == "yaml":
                spec_yaml = str(snippet.input).strip()
                spec_python = yaml.safe_load(spec_yaml)
                spec = json.dumps(json.loads(helpers.read_file(spec_python["data"])))
                spec = spec.replace("'", "\\'")
                self.__count += 1
                map = {"spec": spec, "elem": f"livemark-map-{self.__count}"}
                snippet.output = self.read_asset("markup.html", map=map) + "\n"

    def process_markup(self, markup):
        if self.__count:
            url = "https://unpkg.com"
            markup.add_style(f"{url}/leaflet@1.7.1/dist/leaflet.css")
            markup.add_script(f"{url}/leaflet@1.7.1/dist/leaflet.js")
