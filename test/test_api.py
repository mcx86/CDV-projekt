import pytest
import requests
from api import get_station


# Test dla poprawnej odpowiedzi API
def test_get_station_success(monkeypatch):
    # Przykładowa symulowana odpowiedź API
    mock_response_data = [
        {"id": 1, "stationName": "Station 1", "sensorType": "PM10"},
        {"id": 2, "stationName": "Station 2", "sensorType": "PM2.5"}
    ]

    # Funkcja mockująca zamiast requests.get
    class MockResponse:
        @staticmethod
        def json():
            return mock_response_data

        @property
        def status_code(self):
            return 200

        def raise_for_status(self):
            pass  # Nie rzucamy błędów, bo odpowiedź jest prawidłowa

    # Funkcja, która zastąpi requests.get
    def mock_get(url):
        return MockResponse()

    # Monkeypatchowanie requests.get, żeby używać mock_get
    monkeypatch.setattr(requests, 'get', mock_get)

    # Wywołanie funkcji z przykładowym station_id
    station_id = 1
    result = get_station(station_id)

    # Sprawdzenie, czy odpowiedź funkcji jest zgodna z oczekiwaną symulacją
    assert result == mock_response_data


# Test dla błędu HTTP
def test_get_station_http_error(monkeypatch):
    # Funkcja, która zastąpi requests.get i rzuci wyjątek
    def mock_get(url):
        raise requests.exceptions.HTTPError

    # Monkeypatchowanie requests.get, żeby używać mock_get
    monkeypatch.setattr(requests, 'get', mock_get)

    # Wywołanie funkcji z przykładowym station_id
    station_id = 1

    # Sprawdzenie, czy funkcja rzuca wyjątek HTTPError, gdy serwer zwróci błąd
    with pytest.raises(requests.exceptions.HTTPError):
        get_station(station_id)
