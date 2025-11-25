__all__ = ["settings"]

try:
    from importlib import metadata

    v = metadata.version(__package__)
    __version__ = f"{v}"
except Exception:  # pragma: no cover
    __version__ = "idb"
    pass

from ._settings import settings
