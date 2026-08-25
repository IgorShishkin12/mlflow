import traceback
from typing import Any


def get_stacktrace(error: Any) -> str:
    """Return the repr plus formatted traceback for any raised object."""
    msg = repr(error)
    try:
        tb = traceback.format_exception(error)
        return (msg + "".join(tb)).strip()
    except Exception:
        return msg
