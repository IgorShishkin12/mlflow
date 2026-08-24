from mlflow.protos.model_registry_pb2 import ModelVersionStatus as ProtoModelVersionStatus


class ModelVersionStatus:
    """Enum for status of an :py:class:`mlflow.entities.model_registry.ModelVersion`."""

    PENDING_REGISTRATION: int = ProtoModelVersionStatus.Value("PENDING_REGISTRATION")
    FAILED_REGISTRATION: int = ProtoModelVersionStatus.Value("FAILED_REGISTRATION")
    READY: int = ProtoModelVersionStatus.Value("READY")
    _STRING_TO_STATUS: dict[str, int] = {
        k: ProtoModelVersionStatus.Value(k) for k in ProtoModelVersionStatus.keys()
    }
    _STATUS_TO_STRING = {value: key for key, value in _STRING_TO_STATUS.items()}

    @staticmethod
    def from_string(status_str: str) -> int:
        if status_str not in ModelVersionStatus._STRING_TO_STATUS:
            raise Exception(
                f"Could not get model version status corresponding to string {status_str}. "
                f"Valid status strings: {list(ModelVersionStatus._STRING_TO_STATUS.keys())}"
            )
        return ModelVersionStatus._STRING_TO_STATUS[status_str]

    @staticmethod
    def to_string(status: int) -> str:
        if status not in ModelVersionStatus._STATUS_TO_STRING:
            raise Exception(
                f"Could not get string corresponding to model version status {status}. "
                f"Valid statuses: {list(ModelVersionStatus._STATUS_TO_STRING.keys())}"
            )
        return ModelVersionStatus._STATUS_TO_STRING[status]

    @staticmethod
    def all_status() -> list[int]:
        return list(ModelVersionStatus._STATUS_TO_STRING.keys())
