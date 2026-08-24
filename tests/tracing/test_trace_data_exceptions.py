from pathlib import Path

import pytest

from mlflow.exceptions import MlflowTraceDataCorrupted, MlflowTraceDataNotFound


@pytest.mark.parametrize(
    ("exception_cls", "expected_message"),
    [
        (MlflowTraceDataNotFound, "Trace data not found for path={path}"),
        (MlflowTraceDataCorrupted, "Trace data is corrupted for path={path}"),
    ],
)
def test_trace_data_exception_accepts_pathlib_artifact_path(
    exception_cls: type[MlflowTraceDataNotFound] | type[MlflowTraceDataCorrupted],
    expected_message: str,
) -> None:
    path = Path("some") / "nested" / "trace.json"

    from_path = exception_cls(artifact_path=path)
    assert from_path.message == expected_message.format(path=path)

    from_str = exception_cls(artifact_path=str(path))
    assert from_str.message == expected_message.format(path=path)
    assert from_str.message == from_path.message
