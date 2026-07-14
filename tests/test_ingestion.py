from src.config.settings import DataSourceConfig


def test_url_pattern():
    cfg = DataSourceConfig()
    assert cfg.url_for(2024, 1).endswith("yellow_tripdata_2024-01.parquet")


def test_month_zero_padding():
    cfg = DataSourceConfig()
    assert "2024-03" in cfg.file_name(2024, 3)


def test_local_path(tmp_path):
    cfg = DataSourceConfig(raw_data_dir=tmp_path)
    assert cfg.local_path_for(2023, 12).parent == tmp_path