from livemark import Snippet


# General


def test_snippet():
    snippet = Snippet("input", header=["python", "script"])
    assert snippet.header == ["python", "script"]
    assert snippet.lang == "python"
    assert snippet.type == "script"
    assert snippet.props == {}
    assert snippet.input == "input"
    assert snippet.output is None


def test_snippet_update_output():
    snippet = Snippet("input", header=["python", "script"])
    snippet.output = "output"
    assert snippet.output == "output"


def test_snippet_props():
    snippet = Snippet("input", header=["python", "script", "name1", "name2=value2"])
    assert snippet.props["name1"] is True
    assert snippet.props["name2"] == "value2"
