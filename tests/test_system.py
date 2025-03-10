import json
from pathlib import Path

import pytest

from src.pepyno.converter import convert

FIXTURES_DIR = Path(__file__).parent / "fixtures"
BEHAVE_JSON = FIXTURES_DIR / "behave.json"
EXPECTED_JSON = FIXTURES_DIR / "expected.json"
AUTORETRY_BEHAVE_JSON = FIXTURES_DIR / "autoretry.json"
AUTORETRY_EXPECTED_JSON = FIXTURES_DIR / "autoretry_expected.json"
AUTORETRY_DEDUPE_JSON = FIXTURES_DIR / "autoretry_dedupe.json"


def test_convert():
    """Test basic conversion functionality."""
    with open(BEHAVE_JSON, encoding="utf-8") as f:
        converted = convert(json.load(f))
    with open(EXPECTED_JSON, encoding="utf-8") as f:
        expected_result = json.load(f)
    assert sorted(converted) == sorted(expected_result)


def test_autoretry_convert():
    """Test conversion with auto-retry features."""
    with open(AUTORETRY_BEHAVE_JSON, encoding="utf-8") as f:
        converted = convert(json.load(f))
    with open(AUTORETRY_EXPECTED_JSON, encoding="utf-8") as f:
        expected_result = json.load(f)
    assert sorted(converted) == sorted(expected_result)


def test_dedupe_convert():
    """Test conversion with deduplication enabled."""
    with open(AUTORETRY_BEHAVE_JSON, encoding="utf-8") as f:
        converted = convert(json.load(f), deduplicate=True)
    with open(AUTORETRY_DEDUPE_JSON, encoding="utf-8") as f:
        expected_result = json.load(f)
    assert sorted(converted) == sorted(expected_result)


def test_ids_are_unique():
    """Test that all IDs in the converted output are unique."""
    with open(BEHAVE_JSON, encoding="utf-8") as f:
        converted = convert(json.load(f))
        ids = []
        for feature in converted:
            ids.append(feature["id"])
            for element in feature["elements"]:
                ids.append(element["id"])
    assert len(set(ids)) == 5


@pytest.fixture
def behave_json():
    """Fixture that provides the behave JSON data."""
    with open(BEHAVE_JSON, encoding="utf8") as f:
        return json.load(f)


@pytest.fixture
def autoretry_json():
    """Fixture that provides the autoretry JSON data."""
    with open(AUTORETRY_BEHAVE_JSON, encoding="utf-8") as f:
        return json.load(f)


# Example of a parametrized test using fixtures
@pytest.mark.parametrize("deduplicate", [False, True])
def test_parametrized_convert(behave_json, deduplicate):
    """Example of a parametrized test demonstrating both with and without deduplication."""
    converted = convert(behave_json, deduplicate=deduplicate)
    assert isinstance(converted, list)
    assert len(converted) > 0
