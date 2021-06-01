from typer.testing import CliRunner
from publix import program, __version__

runner = CliRunner()


# General


def test_program():
    result = runner.invoke(program)
    assert result.exit_code == 2
    assert result.stdout.count("Usage")


def test_program_version():
    result = runner.invoke(program, "--version")
    assert result.exit_code == 0
    assert result.stdout.count(__version__)
