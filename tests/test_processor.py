from livemark import Processor, Document


# General


def test_processor():
    document = Document("index.md", target="index.html")
    processor = Processor()
    document = processor.process(document)
    assert document
