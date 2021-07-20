import datetime

import arrow
import pytest

from backend.core.models import PAIRS
from backend.core.tests.factories import HistoricFactory


class TestMmsApiGet:
    @pytest.fixture
    def historic(self, db):
        historic = HistoricFactory()
        historic.save()
        return historic

    def test_mms_invalid_filter_from_must_return_422(self, client):
        resp = client.get("/v1/BRLBTC/mms?from=1&range=200", content_type="application/json")
        assert resp.status_code == 422

    def test_mms_invalid_filter_to_must_return_422(self, client):
        resp = client.get("/v1/BRLBTC/mms?to=1&range=200", content_type="application/json")
        assert resp.status_code == 422

    def test_mms_filter_from_prior_to_365_must_return_422(self, client):
        ts_from = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=400)))
        resp = client.get(f"/v1/BRLBTC/mms?from={ts_from}&range=1", content_type="application/json")
        assert resp.status_code == 422

    def test_mms_invalid_filter_range_must_return_422(self, client):
        resp = client.get("/v1/BRLBTC/mms?range=1", content_type="application/json")
        assert resp.status_code == 422

    def test_mms_status_code_200(self, client, historic):
        resp = client.get(f"/v1/{PAIRS.BRLBTC.value}/mms?range=200", content_type="application/json")
        assert resp.status_code == 200

    def test_mms_200_return_valid_mms(self, client, historic):
        ts_from = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=2)))
        resp = client.get(f"/v1/{PAIRS.BRLBTC.value}/mms?from={ts_from}&range=200", content_type="application/json")
        expected = [{"timestamp": historic.timestamp, "mms": historic.mms_200}]
        assert resp.json() == expected

    def test_no_value_in_database_return_empty(self, client, db):
        ts_from = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=2)))
        resp = client.get(f"/v1/{PAIRS.BRLETH.value}/mms?from={ts_from}&range=200", content_type="application/json")
        expected = []
        assert resp.json() == expected

    def test_return_two_timestamp(self, client, db):
        for i in range(1, 3):
            timestamp = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=i)))
            historic = HistoricFactory(timestamp=timestamp)
            historic.save()

        ts_from = int(datetime.datetime.timestamp(arrow.now().floor("day").datetime - datetime.timedelta(days=2)))
        resp = client.get(f"/v1/{PAIRS.BRLBTC.value}/mms?from={ts_from}&range=200", content_type="application/json")

        assert len(resp.json()) == 2
