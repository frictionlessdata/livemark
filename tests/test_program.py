import pytest
from typer.testing import CliRunner
from livemark import program, __version__

runner = CliRunner()


# General


@pytest.mark.skip
def test_program():
    result = runner.invoke(program, "bad")
    assert result.exit_code == 2
    assert result.stdout.count("Usage")


def test_program_version():
    result = runner.invoke(program, "--version")
    assert result.exit_code == 0
    assert result.stdout.count(__version__)
