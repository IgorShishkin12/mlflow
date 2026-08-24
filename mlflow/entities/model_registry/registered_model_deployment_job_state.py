from mlflow.protos.databricks_uc_registry_messages_pb2 import DeploymentJobConnection


class RegisteredModelDeploymentJobState:
    """Enum for registered model deployment state of an
    :py:class:`mlflow.entities.model_registry.RegisteredModel`.
    """

    NOT_SET_UP: int = DeploymentJobConnection.State.Value("NOT_SET_UP")
    CONNECTED: int = DeploymentJobConnection.State.Value("CONNECTED")
    NOT_FOUND: int = DeploymentJobConnection.State.Value("NOT_FOUND")
    REQUIRED_PARAMETERS_CHANGED: int = DeploymentJobConnection.State.Value(
        "REQUIRED_PARAMETERS_CHANGED"
    )
    _STRING_TO_STATE = {
        k: DeploymentJobConnection.State.Value(k) for k in DeploymentJobConnection.State.keys()
    }
    _STATE_TO_STRING = {value: key for key, value in _STRING_TO_STATE.items()}

    @staticmethod
    def from_string(state_str: str) -> int:
        if state_str not in RegisteredModelDeploymentJobState._STRING_TO_STATE:
            raise Exception(
                f"Could not get deployment job connection state corresponding to string "
                f"{state_str}. "
                f"Valid state strings: {RegisteredModelDeploymentJobState.all_states()}"
            )
        state: int = RegisteredModelDeploymentJobState._STRING_TO_STATE[state_str]
        return state

    @staticmethod
    def to_string(state: int) -> str:
        if state not in RegisteredModelDeploymentJobState._STATE_TO_STRING:
            raise Exception(
                f"Could not get string corresponding to deployment job connection {state}. "
                f"Valid states: {RegisteredModelDeploymentJobState.all_states()}"
            )
        # The lookup table values come from the untyped protobuf enum wrapper, so bind through a
        # typed local before returning.
        state_str: str = RegisteredModelDeploymentJobState._STATE_TO_STRING[state]
        return state_str

    @staticmethod
    def all_states() -> list[int]:
        return list(RegisteredModelDeploymentJobState._STATE_TO_STRING.keys())
