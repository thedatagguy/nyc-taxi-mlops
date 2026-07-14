import pyarrow.parquet as pq

schema_2023 = pq.read_schema("data/raw/yellow_tripdata_2023-01.parquet")
schema_2024 = pq.read_schema("data/raw/yellow_tripdata_2024-01.parquet")

all_field_names = sorted(set(schema_2023.names) | set(schema_2024.names))

for name in all_field_names:
    type_2023 = str(schema_2023.field(name).type) if name in schema_2023.names else "ABSENT"
    type_2024 = str(schema_2024.field(name).type) if name in schema_2024.names else "ABSENT"
    print(f"{name:28s} 2023: {type_2023:15s} 2024: {type_2024}")