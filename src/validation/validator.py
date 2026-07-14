import logging
from pathlib import Path

import pyarrow.parquet as pq

from src.validation.contracts import EXPECTED_COLUMNS

logger = logging.getLogger(__name__)


class SchemaValidationError(Exception):
    pass


def normalize_column(name: str) -> str:
    return name.strip().lower()


def validate_parquet_schema(path: Path) -> dict:
    """Validate a raw monthly file's schema against the contract.

    Returns a report dict; raises SchemaValidationError on hard failures.
    """
    schema = pq.read_schema(path)
    actual = {normalize_column(c) for c in schema.names}
    expected = {normalize_column(c) for c in EXPECTED_COLUMNS}

    missing = expected - actual
    extra = actual - expected

    report = {
        "file": str(path),
        "n_columns": len(schema.names),
        "missing_columns": sorted(missing),
        "unexpected_columns": sorted(extra),
        "dtypes": {name: str(schema.field(name).type) for name in schema.names},
    }

    if missing:
        raise SchemaValidationError(f"Missing required columns in {path.name}: {missing}")
    if extra:
        logger.warning("New/unexpected columns in %s: %s", path.name, extra)

    logger.info("Schema OK: %s", path.name)
    return report