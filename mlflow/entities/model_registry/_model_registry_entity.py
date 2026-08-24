from abc import abstractmethod
from typing import Any, cast

from mlflow.entities._mlflow_object import _MlflowObject


class _ModelRegistryEntity(_MlflowObject):
    @classmethod
    @abstractmethod
    def from_proto(cls, proto: Any) -> "_ModelRegistryEntity":
        pass

    def __eq__(self, other: object) -> bool:
        return dict(self) == dict(cast("_ModelRegistryEntity", other))
