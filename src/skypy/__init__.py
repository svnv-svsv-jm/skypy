# pylint: disable=redefined-builtin
import tomllib

with open("pyproject.toml", "rb") as f:
    _META = tomllib.load(f)

__name__ = _META["tool"]["poetry"]["name"]
__version__ = _META["tool"]["poetry"]["version"]
__description__ = _META["tool"]["poetry"]["description"]
