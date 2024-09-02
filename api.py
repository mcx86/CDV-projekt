import requests


def get_all():
    """Metoda do pobierania wszystkich stacji z API"""
    response = requests.get(f'https://api.gios.gov.pl/pjp-api/rest/station/findAll')
    response.raise_for_status()
    return response.json()

def get_station(station_id):
    """Metoda do pobierania czujnikow dla danej stacji z API"""
    response = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}")
    response.raise_for_status()
    return response.json()

def get_sensor(sensor_id):
    """Metoda do pobierania danych dla danego czujnika z API"""
    response = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}")
    response.raise_for_status()
    return response.json()