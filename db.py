from peewee import *


database = SqliteDatabase('gios.db')

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

database.close()
