from mlflow.entities.model_registry._model_registry_entity import _ModelRegistryEntity
from mlflow.protos.model_registry_pb2 import RegisteredModelAlias as ProtoRegisteredModelAlias


class RegisteredModelAlias(_ModelRegistryEntity):
    """Alias object associated with a registered model."""

    def __init__(self, alias: str, version: str) -> None:
        self._alias = alias
        self._version = version

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def alias(self) -> str:
        """String name of the alias."""
        return self._alias

    @property
    def version(self) -> str:
        """String model version number that the alias points to."""
        return self._version

    @classmethod
    def from_proto(cls, proto: ProtoRegisteredModelAlias) -> "RegisteredModelAlias":
        return cls(proto.alias, proto.version)

    def to_proto(self) -> ProtoRegisteredModelAlias:
        alias_proto = ProtoRegisteredModelAlias()
        alias_proto.alias = self.alias
        alias_proto.version = self.version
        return alias_proto
