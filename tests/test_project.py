from livemark import Project


# General


def test_project():
    project = Project(source="index.md")
    assert project.document.source == "index.md"


# Read


def test_project_read():
    project = Project(config="livemark.yaml")
    project.read()
    assert project.config["brand"]["text"] == "Livemark"
