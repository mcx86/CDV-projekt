from peewee import *


database = SqliteDatabase('gios.db')

class Station(Model):
    """Klasa Station służąca do zamodelowania w bazie danych tabeli Station. Tabela zawiera informacje o stacjach obslugiwanych przez API GIOŚ"""
    station_id = CharField()
    station_name = CharField()
    gegr_lat = FloatField()
    gegr_lon = FloatField()

    class Meta:
        database = database


class Sensor(Model):
    """Klasa Sensor służąca do zamodelowania w bazie danych tabeli Sensor. Tabela zawiera informacje o czujnikach wchodzących w skład stacji
    obslugiwanych przez API GIOŚ"""
    station_id = ForeignKeyField(Station)
    sensor_id = CharField()
    sensor_param = CharField()

    class Meta:
        database = database


class SensorData(Model):
    """Klasa SensorData służąca do zamodelowania w bazie danych tabeli SensorData. Tabela zawiera dane pochodzące z czujników"""
    sensor_id = ForeignKeyField(Sensor)
    sensor_key = CharField()
    sensor_date = CharField()
    sensor_value = CharField(null=True)

    class Meta:
        database = database

database.close()
