import json
import yaml
from jinja2 import Template
from ...plugin import Plugin
from ...helpers import cached_property


class ChartPlugin(Plugin):
    @cached_property
    def count(self):
        return 0

    def process_snippet(self, snippet):
        if self.document.format != "html":
            return

        # Update snippet
        if snippet.type == "chart":
            if snippet.lang == "yaml":
                spec_yaml = str(snippet.input).strip()
                spec_python = yaml.safe_load(spec_yaml)
                spec = json.dumps(spec_python, ensure_ascii=False)
                spec = spec.replace("'", "\\'")
                template = Template(self.read_asset("markup.html"))
                self.count += 1
                chart = {"spec": spec, "elem": f"livemark-chart-{self.count}"}
                snippet.output = template.render(chart=chart) + "\n"

    def process_markup(self, markup):
        markup.add_script("https://unpkg.com/vega@5.20.2/build/vega.min.js")
        markup.add_script("https://unpkg.com/vega-lite@5.1.0/build/vega-lite.min.js")
        markup.add_script("https://unpkg.com/vega-embed@6.18.2/build/vega-embed.min.js")
