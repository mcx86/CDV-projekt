import api
import db
import panel as pn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_sensors(wybor_zrodla,station_id,error_message):
    sensory_slownik = {}
    try:
        if wybor_zrodla == 'API':
            sensors = api.get_station(station_id=station_id)
            sensory_slownik = {sensor['param']['paramCode']: sensor['id'] for sensor in sensors}
            return sensory_slownik
            error_message.object = f'Status:<div style="color: green;font-weight: bold;">Everything is OK! Data from API</div>'
        else:
            sensors = db.Sensor.select().where(db.Sensor.station_id==station_id)
            sensory_slownik = {sensor.sensor_param: sensor.sensor_id for sensor in sensors}
            return sensory_slownik
            error_message.object = f'Status:<div style="color: green;font-weight: bold;">Everything is OK! Data from DB</div>'
    except Exception as e:
        error_message.object = f'Status:<div style="color: red;font-weight: bold;">Error occured: {e}</div>'

def get_sensor_details(wybor_zrodla,sensor_id,place,error_message):
    try:
        place.clear()
        if wybor_zrodla == 'API':
            sensor = api.get_sensor(sensor_id)
            place.append(pn.Row(f"Sensor: <b>{sensor['key']}</b>", styles=dict(background='WhiteSmoke')))
            place.append(pn.Row(f"Czas pomiaru: {str(sensor['values'][0]['date'])}"))
            place.append(pn.Row(f"Wartość: {str(sensor['values'][0]['value'])}"))
        else:
            sensordata = db.SensorData.select().where(db.SensorData.sensor_id==sensor_id).get()
            place.append(pn.Row(f"Sensor: <b>{sensordata.sensor_key}</b>", styles=dict(background='WhiteSmoke')))
            place.append(pn.Row(f"Czas pomiaru: {str(sensordata.sensor_date)}"))
            place.append(pn.Row(f"Wartość: {str(sensordata.sensor_value)}"))


    except Exception as e:
        error_message.object = f'Status:<div style="color: red;font-weight: bold;">Error occured: {e}</div>'

def sensor_to_dataframe(wybor_zrodla,sensor_id, error_message):
    try:
        if wybor_zrodla == 'API':
            sensor = api.get_sensor(sensor_id=sensor_id)
            error_message.object = f'Status:<div style="color: green;font-weight: bold;">Everything is OK! Data from API</div>'
            if len(sensor['values']) == 0:
                raise Exception('Brak wartości dla czujnika!')
            new_rows = [{'Sensor': sensor['key'], 'Data': i['date'], 'Wartosc': i['value']} for i in sensor['values']]
            df = pd.DataFrame(new_rows)
            return df.sort_values(by='Data')
        else:
            sensor = db.SensorData.select().where(db.SensorData.sensor_id==sensor_id).dicts()
            error_message.object = f'Status:<div style="color: green;font-weight: bold;">Everything is OK! Data from DB</div>'
            if len(sensor)==0:
                raise Exception('Brak wartości dla czujnika!')
            new_rows = [{'Sensor': i['sensor_key'], 'Data': i['sensor_date'], 'Wartosc': i['sensor_value']} for i in sensor]
            df = pd.DataFrame(new_rows)
            df['Wartosc'] = pd.to_numeric(df['Wartosc'])
            return df.sort_values(by='Data')
    except Exception as e:
        error_message.object = f'Status:<div style="color: red;font-weight: bold;">Error occured: {e}</div>'

def draw_plot(df):
    plt.figure(figsize=(10,4.3))
    plt.plot(df['Data'], df['Wartosc'],label=df['Sensor'][0])
    plt.xlabel('Data')
    plt.ylabel('Wartosc')
    plt.title(df['Sensor'][0])
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    return pn.pane.Matplotlib(plt.gcf(), tight=True)


