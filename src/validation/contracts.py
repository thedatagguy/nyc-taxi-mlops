from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RawTripRecord(BaseModel):
    """Contract for one raw yellow-taxi trip record.

    Types reflect what TLC *should* deliver. Columns known to vary
    across months (float in some files, int in others) are declared
    with the widest safe type and coerced during validation.
    """

    VendorID: int
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    passenger_count: Optional[float] = None      # nullable + type varies across months
    trip_distance: float = Field(ge=0)
    RatecodeID: Optional[float] = None           # type varies across months
    store_and_fwd_flag: Optional[str] = None
    PULocationID: int
    DOLocationID: int
    payment_type: int
    fare_amount: float
    total_amount: float
    congestion_surcharge: Optional[float] = None  # absent before 2019
    airport_fee: Optional[float] = None           # absent before 2022; case varies!


EXPECTED_COLUMNS = set(RawTripRecord.model_fields.keys())