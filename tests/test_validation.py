import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from src.validation.validator import validate_parquet_schema, SchemaValidationError


def _write_parquet(path, columns):
    table = pa.table({c: [1] for c in columns})
    pq.write_table(table, path)


def test_missing_column_is_fatal(tmp_path):
    f = tmp_path / "bad.parquet"
    _write_parquet(f, ["VendorID", "trip_distance"])  # far from complete
    with pytest.raises(SchemaValidationError):
        validate_parquet_schema(f)