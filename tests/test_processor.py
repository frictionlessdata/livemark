from livemark import Processor, Document


# General


def test_project():
    document = Document()
    processor = Processor()
    content = processor.process(document)
    assert content
