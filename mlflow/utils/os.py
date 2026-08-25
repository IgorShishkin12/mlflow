import os


def is_windows() -> bool:
    """
    Returns true if the local system/OS name is Windows.

    Returns:
        True if the local system/OS name is Windows.

    """
    return os.name == "nt"
