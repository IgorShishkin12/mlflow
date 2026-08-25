from __future__ import annotations

from typing import cast

from mlflow.entities.model_registry._model_registry_entity import _ModelRegistryEntity
from mlflow.entities.model_registry.model_version_deployment_job_run_state import (
    ModelVersionDeploymentJobRunState,
)
from mlflow.entities.model_registry.registered_model_deployment_job_state import (
    RegisteredModelDeploymentJobState,
)
from mlflow.protos.databricks_uc_registry_messages_pb2 import (
    DeploymentJobConnection,
)
from mlflow.protos.databricks_uc_registry_messages_pb2 import (
    ModelVersionDeploymentJobState as ProtoModelVersionDeploymentJobState,
)
from mlflow.protos.model_registry_pb2 import (
    ModelVersionDeploymentJobState as ProtoRegistryModelVersionDeploymentJobState,
)


class ModelVersionDeploymentJobState(_ModelRegistryEntity):
    """Deployment Job state object associated with a model version."""

    def __init__(
        self,
        job_id: str | None,
        run_id: str | None,
        job_state: str | None,
        run_state: str | None,
        current_task_name: str | None,
    ) -> None:
        self._job_id = job_id
        self._run_id = run_id
        self._job_state = job_state
        self._run_state = run_state
        self._current_task_name = current_task_name

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def job_id(self) -> str | None:
        return self._job_id

    @property
    def run_id(self) -> str | None:
        return self._run_id

    @property
    def job_state(self) -> str | None:
        return self._job_state

    @property
    def run_state(self) -> str | None:
        return self._run_state

    @property
    def current_task_name(self) -> str | None:
        return self._current_task_name

    @classmethod
    def from_proto(
        cls,
        proto: ProtoModelVersionDeploymentJobState | ProtoRegistryModelVersionDeploymentJobState,
    ) -> ModelVersionDeploymentJobState:
        # The registry and Databricks UC protos define structurally identical
        # ModelVersionDeploymentJobState messages; both are accepted here.
        return cls(
            job_id=proto.job_id,
            run_id=proto.run_id,
            job_state=RegisteredModelDeploymentJobState.to_string(proto.job_state),
            run_state=ModelVersionDeploymentJobRunState.to_string(proto.run_state),
            current_task_name=proto.current_task_name,
        )

    def to_proto(self) -> ProtoModelVersionDeploymentJobState:
        state = ProtoModelVersionDeploymentJobState()
        if self.job_id is not None:
            state.job_id = self.job_id
        if self.run_id is not None:
            state.run_id = self.run_id
        # The proto fields are typed as the enums' `ValueType` (a NewType over int), while
        # `from_string` returns a plain `int`, hence the casts.
        if self.job_state is not None:
            state.job_state = cast(
                DeploymentJobConnection.State.ValueType,
                RegisteredModelDeploymentJobState.from_string(self.job_state),
            )
        if self.run_state is not None:
            state.run_state = cast(
                ProtoModelVersionDeploymentJobState.DeploymentJobRunState.ValueType,
                ModelVersionDeploymentJobRunState.from_string(self.run_state),
            )
        if self.current_task_name is not None:
            state.current_task_name = self.current_task_name
        return state
