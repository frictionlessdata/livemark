from livemark import Snippet


# General


def test_snippet():
    snippet = Snippet("input", header="python")
    assert snippet.header == "python"
    assert snippet.source == "input"
    assert snippet.target == ""


def test_snippet_update_target():
    snippet = Snippet("input", header="python")
    snippet.target = "output"
    assert snippet.header == "python"
    assert snippet.source == "input"
    assert snippet.target == "output"
