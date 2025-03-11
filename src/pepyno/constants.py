import tomllib
from pathlib import Path


def get_project_version():
    config = _get_project_config()
    return config["project"]["version"]


def get_project_name():
    config = _get_project_config()
    return config["project"]["name"]


def _get_project_config():
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        return tomllib.load(f)


NAME = get_project_name()
VERSION = get_project_version()
