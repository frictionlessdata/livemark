from livemark import Document


# General


def test_document():
    document = Document("index.md")
    document.read()
    assert document.source == "index.md"
    assert document.target == "index.html"
    assert document.input
    assert document.output is None


def test_document_update_output():
    document = Document("index.md")
    document.read()
    document.output = "output"
    assert document.source == "index.md"
    assert document.input
    assert document.output == "output"


def test_document_with_format():
    document = Document("index.md", format="pdf")
    document.read()
    assert document.source == "index.md"
    assert document.target == "index.pdf"


def test_document_with_config():
    document = Document("index.md", config="livemark.yaml")
    document.read()
    assert document.source == "index.md"
    assert document.config["github"]["repo"] == "livemark"
    assert document.config["pages"]["items"]
    assert document.input
