from livemark import Document


# General


def test_document():
    document = Document()
    assert document.path == "index.md"
    assert document.project.path == ""
    assert document.config["title"] == "Livemark"
    assert document.source


def test_document_update_target():
    document = Document()
    document.target = "output"
    assert document.path == "index.md"
    assert document.project.path == ""
    assert document.config["title"] == "Livemark"
    assert document.source
    assert document.target == "output"
