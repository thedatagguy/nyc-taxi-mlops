from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataSourceConfig(BaseSettings):
    """Configuration for the NYC TLC data source."""

    model_config = SettingsConfigDict(env_prefix="TLC_", env_file=".env", extra="ignore")

    base_url: str = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    dataset: str = "yellow_tripdata"
    raw_data_dir: Path = Path("data/raw")
    download_timeout_seconds: int = Field(default=300, gt=0)
    max_retries: int = Field(default=3, ge=1, le=10)

    def file_name(self, year: int, month: int) -> str:
        return f"{self.dataset}_{year}-{month:02d}.parquet"

    def url_for(self, year: int, month: int) -> str:
        return f"{self.base_url}/{self.file_name(year, month)}"

    def local_path_for(self, year: int, month: int) -> Path:
        return self.raw_data_dir / self.file_name(year, month)


settings = DataSourceConfig()