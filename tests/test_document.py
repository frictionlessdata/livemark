from livemark import Document, Project


# General


def test_document():
    document = Document("index.md", target="index.html")
    assert document.source == "index.md"
    assert document.project is None
    assert document.input


def test_document_update_output():
    document = Document("index.md", target="index.html")
    document.output = "output"
    assert document.source == "index.md"
    assert document.project is None
    assert document.input
    assert document.output == "output"


def test_document_with_project():
    document = Document("index.md", target="index.html", project=Project())
    assert document.source == "index.md"
    assert document.project.path == ""
    assert document.config["title"] == "Livemark"
    assert document.input
