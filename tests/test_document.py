from livemark import Document


# General


def test_document():
    document = Document()
    assert document.source == "index.md"
    assert document.project.path == ""
    assert document.config["title"] == "Livemark"
    assert document.input


def test_document_update_output():
    document = Document()
    document.output = "output"
    assert document.source == "index.md"
    assert document.project.path == ""
    assert document.config["title"] == "Livemark"
    assert document.input
    assert document.output == "output"
