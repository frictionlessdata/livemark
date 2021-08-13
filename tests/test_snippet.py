from livemark import Snippet


# General


def test_snippet():
    snippet = Snippet("input", header=["python", "script", "output"])
    assert snippet.header == ["python", "script", "output"]
    assert snippet.lang == "python"
    assert snippet.type == "script"
    assert snippet.mode == "output"
    assert snippet.input == "input"
    assert snippet.output is None


def test_snippet_update_output():
    snippet = Snippet("input", header=["python", "script"])
    snippet.output = "output"
    assert snippet.output == "output"
