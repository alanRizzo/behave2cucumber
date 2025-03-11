import json
from pathlib import PosixPath

import pytest

from pepyno.cli import main


@pytest.fixture
def sample_output_file(tmp_path):
    return tmp_path / "output.json"


def test_main_no_args(runner):
    result = runner.invoke(main, [])
    assert result.exit_code != 0
    assert "Error: Missing option '--infile' / '-i'" in result.output


def test_main_with_input_file(runner, sample_input_file):
    result = runner.invoke(main, ["-i", str(sample_input_file)])
    assert result.exit_code == 0
    assert "Test Scenario" in result.output


def test_main_with_output_file(runner, sample_input_file, sample_output_file):
    result = runner.invoke(main, ["-i", str(sample_input_file), "-o", str(sample_output_file)])
    assert result.exit_code == 0
    assert sample_output_file.exists()
    with sample_output_file.open() as f:
        data = json.load(f)
        assert data[0]["name"] == "Test Scenario"


def test_main_with_debug_flag(mocker, runner, sample_input_file):
    log_mock = mocker.patch("pepyno.cli.setup_logging")

    result = runner.invoke(main, ["-i", str(sample_input_file), "-d", 5])
    assert result.exit_code == 0
    log_mock.assert_called_once_with(0, PosixPath("./"))


def test_main_keyboard_interrupt(mocker, runner, sample_input_file):
    mocker.patch("pepyno.cli.process_file", side_effect=KeyboardInterrupt)
    result = runner.invoke(main, ["-i", str(sample_input_file)])
    assert result.exit_code == 130


def test_main_unhandled_exception(mocker, runner, sample_input_file):
    mocker.patch("pepyno.cli.process_file", side_effect=Exception("Unexpected Error"))
    result = runner.invoke(main, ["-i", str(sample_input_file)])
    assert result.exit_code == 1
