from typing import Any

from mlflow.entities.model_registry import ModelVersion


class ModelVersionSearch(ModelVersion):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["tags"] = []
        kwargs["aliases"] = []
        super().__init__(*args, **kwargs)

    # Intentionally shadows the read-only `tags`/`aliases` properties inherited from
    # ModelVersion: search results never include them, so attribute access raises instead.
    def tags(self) -> dict[str, str]:  # type: ignore[override]
        raise Exception(
            "UC Model Versions gathered through search_model_versions do not have tags. "
            "Please use get_model_version to obtain an individual version's tags."
        )

    def aliases(self) -> list[str]:  # type: ignore[override]
        raise Exception(
            "UC Model Versions gathered through search_model_versions do not have aliases. "
            "Please use get_model_version to obtain an individual version's aliases."
        )

    def __eq__(self, other: object) -> bool:
        if type(other) in {type(self), ModelVersion}:
            return self.__dict__ == other.__dict__
        return False
