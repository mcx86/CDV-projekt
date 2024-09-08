import pytest
from peewee import SqliteDatabase
from db import Station, Sensor, SensorData

# Tworzymy bazę danych w pamięci
database = SqliteDatabase(':memory:')

@pytest.fixture
def setup_database():
    """Fixture do ustawienia i zniszczenia bazy danych przed i po każdym teście"""
    database.bind([Station, Sensor, SensorData], bind_refs=False, bind_backrefs=False)
    database.connect()
    database.create_tables([Station, Sensor, SensorData])

    yield

    database.drop_tables([Station, Sensor, SensorData])
    database.close()

def test_station_model(setup_database):
    """Test dla modelu Station"""
    # Tworzenie instancji stacji
    station = Station.create(station_id='1', station_name='Station 1', gegr_lat=50.0, gegr_lon=20.0)

    # Sprawdzamy, czy dane zostały zapisane poprawnie
    retrieved_station = Station.get(Station.station_id == '1')
    assert retrieved_station.station_name == 'Station 1'
    assert retrieved_station.gegr_lat == 50.0
    assert retrieved_station.gegr_lon == 20.0

def test_sensor_model(setup_database):
    """Test dla modelu Sensor"""
    # Tworzymy stację
    station = Station.create(station_id='1', station_name='Station 1', gegr_lat=50.0, gegr_lon=20.0)

    # Tworzymy czujnik
    sensor = Sensor.create(station_id=station, sensor_id='101', sensor_param='PM10')

    # Sprawdzamy, czy czujnik został poprawnie zapisany
    retrieved_sensor = Sensor.get(Sensor.sensor_id == '101')
    assert retrieved_sensor.sensor_param == 'PM10'
    assert retrieved_sensor.station_id == station

def test_sensor_data_model(setup_database):
    """Test dla modelu SensorData"""
    # Tworzymy stację i czujnik
    station = Station.create(station_id='1', station_name='Station 1', gegr_lat=50.0, gegr_lon=20.0)
    sensor = Sensor.create(station_id=station, sensor_id='101', sensor_param='PM10')

    # Tworzymy dane czujnika
    sensor_data = SensorData.create(sensor_id=sensor, sensor_key='PM10', sensor_date='2024-01-01', sensor_value='10.0')

    # Sprawdzamy, czy dane czujnika zostały poprawnie zapisane
    retrieved_sensor_data = SensorData.get(SensorData.sensor_id == sensor)
    assert retrieved_sensor_data.sensor_key == 'PM10'
    assert retrieved_sensor_data.sensor_date == '2024-01-01'
    assert retrieved_sensor_data.sensor_value == '10.0'
