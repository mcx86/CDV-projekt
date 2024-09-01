from peewee import *
import requests


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



for station_data in data:
    sensors.append(station_data['id'])
    station = Station.create(
        station_id=station_data['id'],
        station_name=station_data['stationName'],
        gegr_lat=station_data['gegrLat'],
        gegr_lon=station_data['gegrLon']
    )


for i in sensors:
    url_sensor = f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{i}'
    response2 = requests.get(url_sensor)
    data2 = response2.json()
    for j in (data2):
        sensor_id_details.append(j['id'])
        sensor = Sensor.create(
            sensor_id=j['id'],
            station_id=j['stationId'],
            sensor_param=j['param']['paramCode']
        )


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





station.save()
sensor.save()
sensor_data.save()
database.close()