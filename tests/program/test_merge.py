from typer.testing import CliRunner
from livemark import program


runner = CliRunner()


# General


def test_program_merge():
    result = runner.invoke(program, "merge index.md --print")
    assert result.exit_code == 0
    assert result.stdout.count("# Livemark")


def test_program_merge_bad_source():
    result = runner.invoke(program, "merge bad.md --print")
    assert result.exit_code == 1
    assert result.stdout.count("No such file")
