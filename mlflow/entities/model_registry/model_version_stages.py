from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE

STAGE_NONE: str = "None"
STAGE_STAGING: str = "Staging"
STAGE_PRODUCTION: str = "Production"
STAGE_ARCHIVED: str = "Archived"

STAGE_DELETED_INTERNAL: str = "Deleted_Internal"

ALL_STAGES: list[str] = [STAGE_NONE, STAGE_STAGING, STAGE_PRODUCTION, STAGE_ARCHIVED]
DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS: list[str] = [STAGE_STAGING, STAGE_PRODUCTION]
_CANONICAL_MAPPING = {stage.lower(): stage for stage in ALL_STAGES}


def get_canonical_stage(stage: str) -> str:
    key = stage.lower()
    if key not in _CANONICAL_MAPPING:
        raise MlflowException(
            "Invalid Model Version stage: {}. Value must be one of {}.".format(
                stage, ", ".join(ALL_STAGES)
            ),
            INVALID_PARAMETER_VALUE,
        )
    return _CANONICAL_MAPPING[key]
