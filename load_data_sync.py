import requests
import time
from peewee import *



start_time = time.time()

database = SqliteDatabase('gios.db')

sensors = []
sensor_id_details = []



class Station(Model):
    station_id = CharField()
    station_name = CharField()
    gegr_lat = FloatField()
    gegr_lon = FloatField()

    class Meta:
        database = database


class Sensor(Model):
    station_id = ForeignKeyField(Station)
    sensor_id = CharField()
    sensor_param = CharField()

    class Meta:
        database = database



class SensorData(Model):
    sensor_id = ForeignKeyField(Sensor)
    sensor_key = CharField()
    sensor_date = CharField()
    sensor_value = CharField(null=True)

    class Meta:
        database = database



database.drop_tables([Station, Sensor, SensorData])
database.create_tables([Station, Sensor, SensorData])

# URL API GIOŚ
url_stations_all = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'



# Pobranie danych z API
response = requests.get(url_stations_all)
data = response.json()



#Tworzenie listy czujnikow - wersja list comprehension
sensors = [station_data['id'] for station_data in data]


#Zapisywanie stacji do bazy - wersja list comprehension
stations = [Station.create(
        station_id=station_data['id'],
        station_name=station_data['stationName'],
        gegr_lat=station_data['gegrLat'],
        gegr_lon=station_data['gegrLon']
    ) for station_data in data]

for station in stations:
    station.save()



#Tworzenie listy z danymi z czujnikow - wersja list comprehension
sensor_id_details = [j['id'] for i in sensors for j in requests.get(f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{i}').json()]


#Zapisywanie czujnikow do bazy - wersja list comprehension
sensors = [
    Sensor.create(
        sensor_id=j['id'],
        station_id=j['stationId'],
        sensor_param=j['param']['paramCode']
    ) for i in sensors for j in requests.get(f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{i}').json()
]

for sensor in sensors:
    sensor.save()


#Zapisywanie  danych z czujnikow do bazy
for i in sensor_id_details:
    url_sensor = f'https://api.gios.gov.pl/pjp-api/rest/data/getData/{i}'
    response3 = requests.get(url_sensor)
    data3 = response3.json()
    for j in (data3['values']):
        sensor_data = SensorData.create(
            sensor_id = i,
            sensor_key=data3['key'],
            sensor_date=j['date'],
            sensor_value = j['value']
        )

sensor_data.save()
database.close()


print('Dane zaladowano w ciagu: %s sekund' % (time.time() - start_time))