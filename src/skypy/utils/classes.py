__all__ = ["get_all_subclasses"]

import typing as ty


def get_all_subclasses(
    base_class: ty.Type[ty.Any],
    only_direct: bool = True,
) -> ty.List[ty.Type]:
    """Finds subclasses of a base class.

    Args:
        base_class (ty.Type): _description_

    Returns:
        ty.List[ty.Type]:
            List of subclasses of base class.
    """
    # Also find sub-subclasses
    subclasses = []

    for subclass in base_class.__subclasses__():
        subclasses.append(subclass)
        if not only_direct:
            subclasses.extend(get_all_subclasses(subclass, only_direct=False))

    return subclasses
