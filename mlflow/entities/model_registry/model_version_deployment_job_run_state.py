from mlflow.protos.databricks_uc_registry_messages_pb2 import (
    ModelVersionDeploymentJobState as ProtoModelVersionDeploymentJobState,
)


class ModelVersionDeploymentJobRunState:
    """Enum for model version deployment state of an
    :py:class:`mlflow.entities.model_registry.ModelVersion`.
    """

    NO_VALID_DEPLOYMENT_JOB_FOUND: int = (
        ProtoModelVersionDeploymentJobState.DeploymentJobRunState.Value(
            "NO_VALID_DEPLOYMENT_JOB_FOUND"
        )
    )
    RUNNING: int = ProtoModelVersionDeploymentJobState.DeploymentJobRunState.Value("RUNNING")
    SUCCEEDED: int = ProtoModelVersionDeploymentJobState.DeploymentJobRunState.Value("SUCCEEDED")
    FAILED: int = ProtoModelVersionDeploymentJobState.DeploymentJobRunState.Value("FAILED")
    PENDING: int = ProtoModelVersionDeploymentJobState.DeploymentJobRunState.Value("PENDING")
    _STRING_TO_STATE: dict[str, int] = {
        k: ProtoModelVersionDeploymentJobState.DeploymentJobRunState.Value(k)
        for k in ProtoModelVersionDeploymentJobState.DeploymentJobRunState.keys()
    }
    _STATE_TO_STRING = {value: key for key, value in _STRING_TO_STATE.items()}

    @staticmethod
    def from_string(state_str: str) -> int:
        if state_str not in ModelVersionDeploymentJobRunState._STRING_TO_STATE:
            raise Exception(
                f"Could not get deployment job run state corresponding to string {state_str}. "
                f"Valid state strings: {ModelVersionDeploymentJobRunState.all_states()}"
            )
        return ModelVersionDeploymentJobRunState._STRING_TO_STATE[state_str]

    @staticmethod
    def to_string(state: int) -> str:
        if state not in ModelVersionDeploymentJobRunState._STATE_TO_STRING:
            raise Exception(
                f"Could not get string corresponding to deployment job run {state}. "
                f"Valid states: {ModelVersionDeploymentJobRunState.all_states()}"
            )
        return ModelVersionDeploymentJobRunState._STATE_TO_STRING[state]

    @staticmethod
    def all_states() -> list[int]:
        return list(ModelVersionDeploymentJobRunState._STATE_TO_STRING.keys())
