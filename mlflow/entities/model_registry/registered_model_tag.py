from mlflow.entities.model_registry._model_registry_entity import _ModelRegistryEntity
from mlflow.protos.model_registry_pb2 import RegisteredModelTag as ProtoRegisteredModelTag


class RegisteredModelTag(_ModelRegistryEntity):
    """Tag object associated with a registered model."""

    def __init__(self, key: str, value: str) -> None:
        self._key = key
        self._value = value

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def key(self) -> str:
        """String name of the tag."""
        return self._key

    @property
    def value(self) -> str:
        """String value of the tag."""
        return self._value

    @classmethod
    def from_proto(cls, proto: ProtoRegisteredModelTag) -> "RegisteredModelTag":
        return cls(proto.key, proto.value)

    def to_proto(self) -> ProtoRegisteredModelTag:
        tag = ProtoRegisteredModelTag()
        tag.key = self.key
        tag.value = self.value
        return tag
