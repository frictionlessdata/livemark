from livemark import Snippet


# General


def test_snippet():
    snippet = Snippet("input", header="python", format="html")
    assert snippet.header == "python"
    assert snippet.format == "html"
    assert snippet.input == "input"
    assert snippet.output == ""


def test_snippet_update_output():
    snippet = Snippet("input", header="python", format="html")
    snippet.output = "output"
    assert snippet.header == "python"
    assert snippet.format == "html"
    assert snippet.input == "input"
    assert snippet.output == "output"
