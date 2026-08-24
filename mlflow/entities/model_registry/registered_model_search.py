from typing import Any

from mlflow.entities.model_registry import RegisteredModel


class RegisteredModelSearch(RegisteredModel):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["tags"] = []
        kwargs["aliases"] = []
        super().__init__(*args, **kwargs)

    # Intentionally shadows the read-only `tags`/`aliases` properties inherited from
    # RegisteredModel: search results never include them, so attribute access raises instead.
    def tags(self) -> dict[str, str]:  # type: ignore[override]
        raise Exception(
            "UC Registered Models gathered through search_registered_models do not have tags. "
            "Please use get_registered_model to obtain an individual model's tags."
        )

    def aliases(self) -> dict[str, str]:  # type: ignore[override]
        raise Exception(
            "UC Registered Models gathered through search_registered_models do not have aliases. "
            "Please use get_registered_model to obtain an individual model's aliases."
        )

    def __eq__(self, other: object) -> bool:
        if type(other) in {type(self), RegisteredModel}:
            return self.__dict__ == other.__dict__
        return False
