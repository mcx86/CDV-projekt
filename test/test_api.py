import pytest
import requests
from api import get_station



def test_get_station_success(monkeypatch):

    mock_response_data = [
        {"id": 1, "stationName": "Station 1", "sensorType": "PM10"},
        {"id": 2, "stationName": "Station 2", "sensorType": "PM2.5"}
    ]


    class MockResponse:
        @staticmethod
        def json():
            return mock_response_data

        @property
        def status_code(self):
            return 200

        def raise_for_status(self):
            pass


    def mock_get(url):
        return MockResponse()


    monkeypatch.setattr(requests, 'get', mock_get)


    station_id = 1
    result = get_station(station_id)


    assert result == mock_response_data



def test_get_station_http_error(monkeypatch):

    def mock_get(url):
        raise requests.exceptions.HTTPError


    monkeypatch.setattr(requests, 'get', mock_get)


    station_id = 1


    with pytest.raises(requests.exceptions.HTTPError):
        get_station(station_id)
