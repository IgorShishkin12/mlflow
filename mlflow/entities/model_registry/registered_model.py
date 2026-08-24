from typing import cast

from mlflow.entities.model_registry._model_registry_entity import _ModelRegistryEntity
from mlflow.entities.model_registry.model_version import ModelVersion
from mlflow.entities.model_registry.registered_model_alias import RegisteredModelAlias
from mlflow.entities.model_registry.registered_model_deployment_job_state import (
    RegisteredModelDeploymentJobState,
)
from mlflow.entities.model_registry.registered_model_tag import RegisteredModelTag

# Import from the defining module; `mlflow.entities.model_registry.prompt_version` re-imports
# this constant without declaring it in `__all__`.
from mlflow.prompt.constants import IS_PROMPT_TAG_KEY
from mlflow.protos.model_registry_pb2 import (
    DeploymentJobConnection as ProtoDeploymentJobConnection,
)
from mlflow.protos.model_registry_pb2 import RegisteredModel as ProtoRegisteredModel
from mlflow.protos.model_registry_pb2 import RegisteredModelAlias as ProtoRegisteredModelAlias
from mlflow.protos.model_registry_pb2 import RegisteredModelTag as ProtoRegisteredModelTag
from mlflow.utils.workspace_utils import resolve_entity_workspace_name


class RegisteredModel(_ModelRegistryEntity):
    """
    MLflow entity for Registered Model.
    """

    def __init__(
        self,
        name: str,
        creation_timestamp: int | None = None,
        last_updated_timestamp: int | None = None,
        description: str | None = None,
        latest_versions: list[ModelVersion] | None = None,
        tags: list[RegisteredModelTag] | None = None,
        aliases: list[RegisteredModelAlias] | None = None,
        deployment_job_id: str | None = None,
        deployment_job_state: str | None = None,
        workspace: str | None = None,
    ) -> None:
        # Constructor is called only from within the system by various backend stores.
        super().__init__()
        self._name = name
        self._creation_time = creation_timestamp
        self._last_updated_timestamp = last_updated_timestamp
        self._description = description
        self._latest_version = latest_versions
        self._tags = {tag.key: tag.value for tag in (tags or [])}
        self._aliases = {alias.alias: alias.version for alias in (aliases or [])}
        self._deployment_job_id = deployment_job_id
        self._deployment_job_state = deployment_job_state
        self._workspace = resolve_entity_workspace_name(workspace)

    @property
    def name(self) -> str:
        """String. Registered model name."""
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def creation_timestamp(self) -> int | None:
        """Integer. Model version creation timestamp (milliseconds since the Unix epoch)."""
        return self._creation_time

    @property
    def last_updated_timestamp(self) -> int | None:
        """Integer. Timestamp of last update for this model version (milliseconds since the Unix
        epoch).
        """
        return self._last_updated_timestamp

    @last_updated_timestamp.setter
    def last_updated_timestamp(self, updated_timestamp: int):
        self._last_updated_timestamp = updated_timestamp

    @property
    def description(self) -> str | None:
        """String. Description"""
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def latest_versions(self) -> list[ModelVersion] | None:
        """List of the latest :py:class:`mlflow.entities.model_registry.ModelVersion` instances
        for each stage.
        """
        return self._latest_version

    @latest_versions.setter
    def latest_versions(self, latest_versions: list[ModelVersion]):
        self._latest_version = latest_versions

    @property
    def tags(self) -> dict[str, str]:
        """Dictionary of tag key (string) -> tag value for the current registered model."""
        # Remove the is_prompt tag as it should not be user-facing
        return {k: v for k, v in self._tags.items() if k != IS_PROMPT_TAG_KEY}

    def _is_prompt(self):
        """Check if the registered model is a prompt."""
        return self._tags.get(IS_PROMPT_TAG_KEY, "false").lower() == "true"

    @property
    def aliases(self) -> dict[str, str]:
        """Dictionary of aliases (string) -> version for the current registered model."""
        return self._aliases

    @property
    def workspace(self) -> str:
        """Workspace name for the registered model."""
        return self._workspace

    @classmethod
    def _properties(cls):
        # aggregate with base class properties since cls.__dict__ does not do it automatically
        return sorted(cls._get_properties_helper())

    def _add_tag(self, tag):
        self._tags[tag.key] = tag.value

    def _add_alias(self, alias):
        self._aliases[alias.alias] = alias.version

    @property
    def deployment_job_id(self) -> str | None:
        """Deployment job ID for the current registered model."""
        return self._deployment_job_id

    @deployment_job_id.setter
    def deployment_job_id(self, deployment_job_id: str):
        self._deployment_job_id = deployment_job_id

    @property
    def deployment_job_state(self) -> str | None:
        """Deployment job state for the current registered model."""
        return self._deployment_job_state

    # proto mappers
    @classmethod
    def from_proto(cls, proto: ProtoRegisteredModel) -> "RegisteredModel":
        # input: mlflow.protos.model_registry_pb2.RegisteredModel
        # returns RegisteredModel entity
        registered_model = cls(
            proto.name,
            proto.creation_timestamp,
            proto.last_updated_timestamp,
            proto.description,
            [ModelVersion.from_proto(mvd) for mvd in proto.latest_versions],
        )
        for tag in proto.tags:
            registered_model._add_tag(RegisteredModelTag.from_proto(tag))
        for alias in proto.aliases:
            registered_model._add_alias(RegisteredModelAlias.from_proto(alias))
        registered_model._deployment_job_id = proto.deployment_job_id
        registered_model._deployment_job_state = RegisteredModelDeploymentJobState.to_string(
            proto.deployment_job_state
        )
        return registered_model

    def to_proto(self) -> ProtoRegisteredModel:
        # returns mlflow.protos.model_registry_pb2.RegisteredModel
        rmd = ProtoRegisteredModel()
        rmd.name = self.name
        if self.creation_timestamp is not None:
            rmd.creation_timestamp = self.creation_timestamp
        if self.last_updated_timestamp:
            rmd.last_updated_timestamp = self.last_updated_timestamp
        if self.description:
            rmd.description = self.description
        if self.latest_versions is not None:
            rmd.latest_versions.extend([
                model_version.to_proto() for model_version in self.latest_versions
            ])
        if self.deployment_job_id:
            rmd.deployment_job_id = self.deployment_job_id
        if self.deployment_job_state:
            # The generated pb2 stubs type proto enum fields as EnumTypeWrapper subclasses, so
            # cast the plain int returned by from_string to the proto enum type of this field.
            rmd.deployment_job_state = cast(
                ProtoDeploymentJobConnection.State,
                RegisteredModelDeploymentJobState.from_string(self.deployment_job_state),
            )
        rmd.tags.extend([
            ProtoRegisteredModelTag(key=key, value=value) for key, value in self._tags.items()
        ])
        rmd.aliases.extend([
            ProtoRegisteredModelAlias(alias=alias, version=str(version))
            for alias, version in self._aliases.items()
        ])
        return rmd
