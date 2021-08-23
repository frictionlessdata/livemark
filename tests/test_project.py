from livemark import Project


# General


def test_project():
    project = Project(config="livemark.yaml")
    assert project.config["brand"]["text"] == "Livemark"
