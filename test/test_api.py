import pytest
import requests


from api import get_all, get_station, get_sensor


mock_station_data = [
    {"id": 1, "stationName": "Station 1"},
    {"id": 2, "stationName": "Station 2"}
]

mock_sensor_data = [
    {"id": 101, "stationId": 1, "param": {"paramName": "PM10"}},
    {"id": 102, "stationId": 1, "param": {"paramName": "PM2.5"}}
]

mock_sensor_readings = {
    "key": "PM10",
    "values": [{"date": "2024-01-01", "value": 10.0}]
}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"HTTP Error: {self.status_code}")


def test_get_all(monkeypatch):

    def mock_get(url):
        assert url == 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
        return MockResponse(mock_station_data, 200)


    monkeypatch.setattr(requests, 'get', mock_get)


    result = get_all()


    assert result == mock_station_data


def test_get_station(monkeypatch):

    def mock_get(url):
        station_id = 1
        assert url == f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}'
        return MockResponse(mock_sensor_data, 200)


    monkeypatch.setattr(requests, 'get', mock_get)


    station_id = 1
    result = get_station(station_id)


    assert result == mock_sensor_data


def test_get_sensor(monkeypatch):

    def mock_get(url):
        sensor_id = 101
        assert url == f'https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}'
        return MockResponse(mock_sensor_readings, 200)


    monkeypatch.setattr(requests, 'get', mock_get)


    sensor_id = 101
    result = get_sensor(sensor_id)


    assert result == mock_sensor_readings
