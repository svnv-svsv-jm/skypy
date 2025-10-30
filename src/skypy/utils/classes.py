__all__ = ["get_all_subclasses"]

import typing as ty


def get_all_subclasses(
    base_class: type[ty.Any],
    only_direct: bool = True,
) -> list[type]:
    """Finds subclasses of a base class.

    Args:
        base_class (type):
            Base class to find subclasses of.

        only_direct (bool):
            If `True`, only find direct subclasses.

    Returns:
        list[type]:
            List of subclasses of base class.
    """
    # Also find sub-subclasses
    subclasses = []

    for subclass in base_class.__subclasses__():
        subclasses.append(subclass)
        if not only_direct:
            subclasses.extend(get_all_subclasses(subclass, only_direct=False))

    return subclasses
