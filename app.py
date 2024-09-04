import folium
import api
import panel as pn
import db
import helper as hp


#Inicjalizacja panelu
pn.extension(sizing_mode="stretch_width")



#Panel mapa
m = folium.Map(location=[52.21, 20.00], zoom_start=6)
folium_pane = pn.pane.plot.Folium(m,sizing_mode='stretch_both')
folium_pane.object = m



#Panel statusu/bledu
error_message = pn.pane.HTML(sizing_mode='stretch_both')


#Panel szczegolow
details = pn.pane.HTML(sizing_mode='stretch_both')


#Inicjalizacja widgetow
input = pn.widgets.TextInput(name='Podaj ID stacji', placeholder='Podaj ID stacji z pinezki na mapie...')
wybor_zrodla = pn.widgets.RadioBoxGroup(name='Data Source', options=['API','DB'],inline=True)
id_czujnik = pn.widgets.TextInput(name='A widget', value='A string')
button_szukaj = pn.widgets.Button(name='Szukaj', disabled=False)
button_sensor_szczegoly = pn.widgets.Button(name='Sensor szczegoly', disabled=False)
button_pokaz_stacje = pn.widgets.Button(name='Pokaz stacje', disabled=False)
panel_boczny = pn.Column()
details = pn.Column()





def update_panel_boczny(event):
    global wybor_sensora
    panel_boczny.clear()
    details.clear()
    station_id = input.value_input


    sensory = hp.get_sensors(wybor_zrodla.value,station_id=station_id,error_message=error_message)
    wybor_sensora = pn.widgets.Select(name='Dostepne sensory', options=sensory)
    panel_boczny.append(wybor_sensora)
    panel_boczny.append(button_sensor_szczegoly)





def get_sensor_details(event):
    df = hp.sensor_to_dataframe(wybor_zrodla.value, sensor_id=wybor_sensora.value, error_message=error_message)
    hp.get_sensor_details(wybor_zrodla.value,wybor_sensora.value,place=details,df=df,error_message=error_message)
    details.append(hp.draw_plot(df=df))


#Rozmieszczenie znacznikow na mapie
def set_czujniki(event):
    try:
        if wybor_zrodla.value == 'API':
            station_all = api.get_all()
            for item in station_all:
                    folium.Marker(
                    [item['gegrLat'], item['gegrLon']], popup=f"<i>{item['stationName']} ID stacji: {item['id']}</i>",
                    ).add_to(m)
            folium_pane.object = m
            error_message.object = f'Status:<div style="color: green;font-weight: bold;">Everything is OK! Data from API</div>'
        else:
            station_all = db.Station.select()
            for item in station_all:
                folium.Marker(
                    [item.gegr_lat, item.gegr_lon], popup=f"<i>{item.station_name} ID stacji: {item.station_id}</i>",
                ).add_to(m)
            folium_pane.object = m
            error_message.object = f'Status:<div style="color: green;font-weight: bold;">Everything is OK! Data from DB</div>'

    except Exception as e:
            error_message.object = f'Status:<div style="color: red;font-weight: bold;">Error occured: {e}</div>'



#Metoda do aktualizacji sidebara
button_szukaj.on_click(update_panel_boczny)
button_sensor_szczegoly.on_click(get_sensor_details)
button_pokaz_stacje.on_click(set_czujniki)




template = pn.template.FastGridTemplate(site="CDV", title="Jakość powietrza w Polsce",sidebar=[wybor_zrodla,button_pokaz_stacje,input,button_szukaj,panel_boczny], prevent_collision=True)
template.main[0:4,0:5] = folium_pane
template.main[0:6,5:12] = details
template.main[4:6,0:5] = error_message




template.servable()
