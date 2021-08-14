import pytest
from livemark import Document, LivemarkException, helpers


# General


def test_document():
    document = Document("index.md")
    assert document.source == "index.md"
    assert document.format == "html"
    assert len(document.plugins) > 20


def test_document_format():
    document = Document("index.md", format="pdf")
    assert document.format == "pdf"
    assert document.source == "index.md"
    assert document.target == "index.pdf"


def test_document_config():
    document = Document("index.md", config="livemark.yaml")
    assert document.source == "index.md"
    assert document.config["github"]["repo"] == "livemark"


def test_document_update_content():
    document = Document("index.md")
    document.content = "new"
    assert document.source == "index.md"
    assert document.content == "new"


def test_document_update_output():
    document = Document("index.md")
    document.output = "output"
    assert document.source == "index.md"
    assert document.output == "output"


# Build


def test_document_build(tmpdir):
    target = str(tmpdir / "index.html")
    document = Document("index.md", target=target)
    output = document.build()
    assert output.count("<h1>Livemark</h1>")
    assert helpers.read_file(target).count("<h1>Livemark</h1>")


def test_document_build_diff():
    document = Document("data/diff.md", target="data/diff.md")
    with helpers.capture_stdout() as stdout:
        document.build(diff=True)
    output = stdout.getvalue().strip()
    assert output.count("+Hello World")


def test_document_build_print():
    document = Document("data/diff.md", target="data/diff.md")
    with helpers.capture_stdout() as stdout:
        document.build(print=True)
    output = stdout.getvalue().strip()
    assert output.count("Hello World")


# Read


def test_document_read():
    document = Document("index.md", config="livemark.yaml")
    document.read()
    assert document.source == "index.md"
    assert document.target == "index.html"
    assert document.config["pages"]["list"]
    assert document.input.count("# Livemark")
    assert document.preface == ""
    assert document.content.count("# Livemark")
    assert document.output is None
    assert document.title == "Livemark"
    assert document.description.startswith("Livemark is a static site generator")
    assert document.keywords == "livemark"


def test_document_read_with_preface():
    document = Document("data/preface.md")
    document.read()
    assert document.preface == "search: true"
    assert document.content == "# Preface"
    assert document.config["search"] == {"self": True}


def test_document_read_with_preface_invalid():
    document = Document("data/invalid.md")
    with pytest.raises(LivemarkException) as excinfo:
        document.read()
    assert str(excinfo.value).count('Invalid "brand" config')


# Process


def test_document_process_not_read():
    document = Document("index.md")
    with pytest.raises(LivemarkException) as excinfo:
        document.process()
    assert str(excinfo.value).count("Read document before processing")


# Write


def test_document_write_not_processed():
    document = Document("index.md")
    document.read()
    with pytest.raises(LivemarkException) as excinfo:
        document.write(print=True)
    assert str(excinfo.value).count("Process document before writing")
