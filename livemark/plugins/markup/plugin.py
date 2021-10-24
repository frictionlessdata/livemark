import marko
import textwrap
from pyquery import PyQuery
from marko.ext.gfm import GFM
from ..html.renderer import HtmlExtension
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
            if snippet.type == "markup" and snippet.lang in ["html", "jsx"]:

                # Html
                if snippet.lang == "html":
                    markdown = marko.Markdown()
                    markdown.use(GFM)
                    markdown.use(HtmlExtension)
                    query = PyQuery(snippet.input)
                    for node in query.find(".livemark-markdown"):
                        node = PyQuery(node)
                        if not node.children():
                            input = node.text(squash_space=False)
                            input = textwrap.dedent(input).strip("\n")
                            output = markdown.convert(input)
                            node.html(output)
                    snippet.output = query.outer_html() + "\n"

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
