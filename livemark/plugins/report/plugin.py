import yaml
from ...plugin import Plugin
from frictionless import Report


# NOTE:
# Improve how we serialize/deseritalize the spec


class ReportPlugin(Plugin):
    identity = "report"
    priority = 60

    # Process

    def process_document(self, document):
        self.__count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "report" and snippet.lang == "yaml":
                spec = yaml.safe_load(str(snippet.input).strip())
                spec = Report(**spec).to_dict()
                self.__count += 1
                report = {"spec": spec, "elem": f"livemark-report-{self.__count}"}
                snippet.output = self.read_asset("markup.html", report=report) + "\n"

    def process_markup(self, markup):
        if self.__count:
            url = "https://unpkg.com/frictionless-components@1.0.1"
            markup.add_style(f"{url}/dist/frictionless-components.min.css")
            markup.add_script(f"{url}/dist/frictionless-components.min.js")
