from livemark import Snippet


# General


def test_snippet():
    snippet = Snippet("input", header=["python"])
    assert snippet.header == ["python"]
    assert snippet.input == "input"
    assert snippet.output is None


def test_snippet_update_output():
    snippet = Snippet("input", header=["python"])
    snippet.output = "output"
    assert snippet.header == ["python"]
    assert snippet.input == "input"
    assert snippet.output == "output"
