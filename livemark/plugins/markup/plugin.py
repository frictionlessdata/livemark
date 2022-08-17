import marko
from marko.ext.gfm import GFM
from ...plugin import Plugin


# NOTE:
# We might consider rebase markdown blocks rendering on using Document
# This change will remove the direct HtmlException and GFM dependencies


class MarkupPlugin(Plugin):
    identity = "markup"
    priority = 60

    # Process

    def process_document(self, document):
        self.__jsx_count = 0

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "markup" and snippet.lang in ["markdown", "html", "jsx"]:

                # Markdown
                if snippet.lang == "markdown":
                    markdown = marko.Markdown()
                    markdown.use(GFM)
                    snippet.output = markdown.convert(snippet.input)

                # Html
                elif snippet.lang == "html":
                    snippet.output = snippet.input

                # Jsx
                elif snippet.lang == "jsx":
                    self.__jsx_count += 1
                    context = {}
                    context["content"] = snippet.input
                    context["element"] = self.__jsx_count
                    snippet.output = self.read_asset("markup.html", **context) + "\n"

    def process_markup(self, markup):
        if self.__jsx_count:
            url = "https://unpkg.com"
            markup.add_script(f"{url}/react@17.0.2/umd/react.production.min.js")
            markup.add_script(f"{url}/react-dom@17.0.2/umd/react-dom.production.min.js")
            markup.add_script(f"{url}/babel-standalone@6.26.0/babel.min.js")
