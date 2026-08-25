from typing import Any, cast

from mlflow.entities._mlflow_object import _MlflowObject


class _ModelRegistryEntity(_MlflowObject):
    @classmethod
    def from_proto(cls, proto: Any) -> Any:
        """Proto-mapping hook; concrete entities override this with precise signatures.

        Not decorated with @abstractmethod: this base class is not an ABC (no ABCMeta),
        so the decorator had no runtime effect; it only forced every concrete entity
        to carry proto-mapping signatures or suppressions.
        """

    def __eq__(self, other: object) -> bool:
        return dict(self) == dict(cast("_ModelRegistryEntity", other))
