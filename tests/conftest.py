import json

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def sample_input_file(tmp_path):
    file_path = tmp_path / "input.json"
    content = [
        {
            "name": "Test Scenario",
            "location": "features/test.feature:12",
            "steps": [{"step": "Given something happens"}],
        }
    ]
    file_path.write_text(json.dumps(content))
    return file_path
