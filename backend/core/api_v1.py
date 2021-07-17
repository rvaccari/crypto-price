import datetime
from typing import Optional, List

import arrow
from ninja import Router, Schema, Query
from pydantic import Field, validator

from backend.core.models import Historic, PAIRS

router = Router()


def ts_yesterday(value: Optional[int]) -> int:
    return value or int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=1)))


class FiltersMms(Schema):
    ts_from: int = Field(None, alias="from")
    ts_to: int = Field(None, alias="to")
    range: int

    _set_ts_from = validator("ts_from", always=True, allow_reuse=True)(ts_yesterday)
    _set_ts_to = validator("ts_to", always=True, allow_reuse=True)(ts_yesterday)

    @validator("range")
    def set_range(cls, value: int) -> int:
        if value not in [20, 50, 200]:
            raise ValueError("range must be 20, 50 or 200")
        return value

    @validator("ts_from", "ts_to")
    def check_valid_timestamp(cls, value: Optional[int], values, **kwargs) -> Optional[int]:
        if not value:
            return None

        if value < int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=365))):
            raise ValueError(f"{getattr(kwargs.get('field'), 'alias')} invalid value")

        return value


class HistoricOut(Schema):
    timestamp: int
    mms: float


@router.get("/{pair}/mms", response=List[HistoricOut])
def mms(request, pair: PAIRS, filters: FiltersMms = Query(...)):
    histories = Historic.objects.filter(pair=pair).filter(timestamp__range=(filters.ts_from, filters.ts_to))
    mmss = {
        20: "mms_20",
        50: "mms_50",
        200: "mms_200",
    }
    return [HistoricOut(timestamp=x.timestamp, mms=getattr(x, mmss[filters.range])) for x in histories]
