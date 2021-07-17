from livemark import Processor, Document


# General


def test_project():
    document = Document()
    processor = Processor()
    document = processor.process(document)
    assert document
