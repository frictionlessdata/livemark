from livemark import Server, Project


def test_server():
    project = Project(config="livemark.yaml")
    server = Server(project)
    assert server.project is project
