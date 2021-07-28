from livemark import Snippet, Document


# General


def test_snippet():
    document = Document("index.md")
    snippet = Snippet("input", header=["python"], document=document)
    assert snippet.document.format == "html"
    assert snippet.header == ["python"]
    assert snippet.input == "input"
    assert snippet.output == ""


def test_snippet_update_output():
    document = Document("index.md")
    snippet = Snippet("input", header=["python"], document=document)
    snippet.output = "output"
    assert snippet.document.format == "html"
    assert snippet.header == ["python"]
    assert snippet.input == "input"
    assert snippet.output == "output"
