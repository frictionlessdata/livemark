from livemark import Server, Document


def test_server():
    document = Document("index.md")
    server = Server(document)
    assert server.document is document
