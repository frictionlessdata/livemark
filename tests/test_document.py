from livemark import Document, Project


# General


def test_document():
    document = Document("index.md")
    assert document.source == "index.md"
    assert document.target == "index.html"
    assert document.project is None
    assert document.input


def test_document_update_output():
    document = Document("index.md")
    document.output = "output"
    assert document.source == "index.md"
    assert document.project is None
    assert document.input
    assert document.output == "output"


def test_document_with_format():
    document = Document("index.md", format="pdf")
    assert document.source == "index.md"
    assert document.target == "index.pdf"


def test_document_with_project():
    document = Document("index.md", project=Project())
    assert document.source == "index.md"
    assert document.project.path == ""
    assert document.config["github"]["repo"] == "livemark"
    assert document.input
