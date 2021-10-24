import pytest
from typer.testing import CliRunner
from livemark import program


runner = CliRunner()


# General


@pytest.mark.skip
def test_program_build():
    result = runner.invoke(program, "build index.md --print")
    assert result.exit_code == 0
    assert result.stdout.count("<h1>Livemark</h1>")


def test_program_build_bad_source():
    result = runner.invoke(program, "build bad.md --print")
    assert result.exit_code == 1
    assert result.stdout.count("No such file")
