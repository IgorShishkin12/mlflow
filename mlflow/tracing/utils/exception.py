import functools
from typing import Callable, ParamSpec, TypeVar

from mlflow.exceptions import MlflowTracingException

P = ParamSpec("P")
R = TypeVar("R")


def raise_as_trace_exception(f: Callable[P, R]) -> Callable[P, R]:
    """
    A decorator to make sure that the decorated function only raises MlflowTracingException.

    Any exceptions are caught and translated to MlflowTracingException before exiting the function.
    This is helpful for upstream functions to handle tracing related exceptions properly.
    """

    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise MlflowTracingException(e) from e

    return wrapper
