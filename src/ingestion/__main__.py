import argparse
import logging

from src.ingestion.downloader import download_month

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

parser = argparse.ArgumentParser(description="Download one month of NYC TLC trip data")
parser.add_argument("--year", type=int, required=True)
parser.add_argument("--month", type=int, required=True, choices=range(1, 13))
parser.add_argument("--force", action="store_true")
args = parser.parse_args()

download_month(args.year, args.month, force=args.force)