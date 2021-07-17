import datetime

import arrow
from factory.django import DjangoModelFactory

from backend.core.models import Historic, PAIRS


class HistoricFactory(DjangoModelFactory):
    pair = PAIRS.BRLBTC
    timestamp = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=1)))
    price = 5.00
    mms_20 = 6.00
    mms_50 = 7.00
    mms_200 = 8.00

    class Meta:
        model = Historic
