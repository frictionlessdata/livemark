from livemark import Document


# General


def test_project():
    document = Document()
    assert document.path == "index.md"
    assert document.project.path == ""
    assert document.config["title"] == "Livemark"
    assert document.content
