from livemark import Project


# General


def test_project():
    project = Project()
    assert project.path == ""
    assert project.config["brand"]["title"] == "Livemark"
