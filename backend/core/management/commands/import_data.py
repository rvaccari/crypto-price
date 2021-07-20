import datetime

import arrow
import pandas as pd
import requests
from django.core.management import BaseCommand

from backend.core.models import Historic, PAIRS


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Start."))
        start_ts_200 = int(
            datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=565))
        )
        start_ts = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=365)))
        end_ts = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime))

        for pair in PAIRS:

            url = f"https://mobile.mercadobitcoin.com.br/v4/{pair}/candle?from={start_ts_200}&to={end_ts}&precision=1d"
            self.stdout.write(self.style.NOTICE(f"Get data from {url}"))
            resp = requests.get(url)
            if not resp.status_code == 200:
                self.stdout.write(
                    self.style.ERROR(f"Service unavailable. No data in {pair}. Status code {resp.status_code}")
                )
                continue

            pd.options.mode.chained_assignment = None
            candles = pd.DataFrame.from_dict(resp.json()["candles"])
            candles.index = pd.Index(candles.timestamp)

            df = candles[["timestamp", "close"]]
            df["mms_20"] = df.close.rolling(window=20).mean()
            df["mms_50"] = df.close.rolling(window=50).mean()
            df["mms_200"] = df.close.rolling(window=200).mean()
            df_365 = df[df.index > start_ts]

            idx_timestamp = df_365.columns.get_loc("timestamp")
            idx_close = df_365.columns.get_loc("close")
            idx_mms_20 = df_365.columns.get_loc("mms_20")
            idx_mms_50 = df_365.columns.get_loc("mms_20")
            idx_mms_200 = df_365.columns.get_loc("mms_20")

            self.stdout.write(self.style.NOTICE("Saving to database."))
            for d in df_365.values:
                historic, _ = Historic.objects.update_or_create(
                    timestamp=int(d[idx_timestamp]),
                    pair=pair,
                    defaults={
                        "price": d[idx_close],
                        "mms_20": d[idx_mms_20],
                        "mms_50": d[idx_mms_50],
                        "mms_200": d[idx_mms_200],
                    },
                )
                historic.save()
            self.stdout.write(self.style.SUCCESS(f"End import data {pair}."))
        self.stdout.write(self.style.NOTICE(f"End."))
