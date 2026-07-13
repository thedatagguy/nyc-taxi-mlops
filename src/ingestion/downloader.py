import logging
import time
from pathlib import Path

import requests

from src.config.settings import settings

logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """Raised when a monthly file cannot be downloaded after all retries."""


def download_month(year: int, month: int, force: bool = False) -> Path:
    """Download one month of TLC trip data. Returns the local file path.

    Idempotent: skips download if the file already exists (unless force=True).
    """
    dest = settings.local_path_for(year, month)
    url = settings.url_for(year, month)

    if dest.exists() and not force:
        logger.info("File already exists, skipping: %s", dest)
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".parquet.part")

    for attempt in range(1, settings.max_retries + 1):
        try:
            logger.info("Downloading %s (attempt %d/%d)", url, attempt, settings.max_retries)
            with requests.get(url, stream=True, timeout=settings.download_timeout_seconds) as r:
                if r.status_code == 403:
                    # TLC returns 403 for months that don't exist (yet)
                    raise DownloadError(
                        f"{year}-{month:02d} not available (HTTP 403). "
                        "TLC publishes with ~2 month delay."
                    )
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        f.write(chunk)
            tmp.rename(dest)  # atomic-ish: only appears at final path when complete
            logger.info("Saved %s (%.1f MB)", dest, dest.stat().st_size / 1e6)
            return dest
        except DownloadError:
            raise  # don't retry a file that doesn't exist
        except requests.RequestException as e:
            logger.warning("Attempt %d failed: %s", attempt, e)
            if attempt == settings.max_retries:
                raise DownloadError(f"Failed after {settings.max_retries} attempts: {url}") from e
            time.sleep(2 ** attempt)  # exponential backoff

    raise DownloadError(f"Unreachable: {url}")