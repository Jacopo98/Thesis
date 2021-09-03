from datetime import datetime
import matplotlib.pyplot as plt 
from sec_tool.config import DB_NAME, CONF_EDITIONS_LOWER_BOUNDARY

import numpy as np


def create_output(storico_papers):
    x=np.array([date for date in range((2021-CONF_EDITIONS_LOWER_BOUNDARY), 2021)])
    y=np.array(storico_papers)

    z1 = np.polyfit(x, y, 1)
    p = np.poly1d(z1)

    plt.title('Serie Storica numero di pubblicazioni in Italia', fontsize=16)

    plt.xlabel("Anni", size = 16,)
    plt.ylabel("Numero di pubblicazioni", size = 16)

    plt.bar(x,y, color ='blue', width = 0.4)
    plt.plot(x,p(x),"r--")

    plt.gcf().set_size_inches(9, 7)
    plt.xticks(x)                           #visualizzo tutte le date sull'asse x
    plt.show()

    ## FINE ANALISI STORICO

    ### recuperare coordinate sapendo l' indirizzo
    """ from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="tutorial")
    # get location raw data
    location = geolocator.geocode("University of Bergamo").raw

    latitude = location["lat"]
    longitude = location["lon"]
    print(f"{latitude}, {longitude}") """


    ## CREAZIONE MAPPA DI CALORE ##

    import folium
    from folium import plugins
    import pandas as pd
    import webbrowser

    centridiricerca = pd.read_csv('data/centridiricerca.csv')
    coordinate = pd.read_csv('data/coordinate.csv', delimiter = ';', header = 0, index_col = 0)

    # combine and keep the first instance of id
    centri = pd.concat([centridiricerca], axis=0).drop_duplicates(subset=['id'])

    centri.head()

    m = folium.Map([42.081676, 11.803739], zoom_start=6)

    coll=[]
    coll_molt=[]

    for t in range(1,(len(coordinate['coordinate_coppia'])+1)):
        coll_x=coordinate['coordinate_coppia'][t]
        coll_xc = eval(coll_x)
        coll.append(coll_xc)
        valore=coordinate['valore'][t]
        coll_molt.append(int(valore))

    # Inserisco un marcatore circolare per ogni gruppo per visualizzare un popup premendo su esso
    valori = []
    for index, row in centri.iterrows():
        valori.append(row['num_papers'])
        name= row['name']
        iframe = folium.IFrame(name)
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        folium.CircleMarker([row['latitude'], row['longitude']],
                            popup=popup,
                            fill_color="#3db7e4", # divvy color
                            opacity=0.2,
                        ).add_to(m)

    #print(valori)

    for i in range(1,18):   #numeri da 1 a 17
        sedi = centri.iloc[(i-1):i][['latitude', 'longitude']].to_numpy() 
        m.add_child(plugins.HeatMap(sedi, radius=(valori[i-1]*5)))

    #il seguente è il modo per dare un raggio ad ogni bolla della dimensione del numero di pubblicazioni fatte dal gruppo
    #LO SVANTAGGIO è che inserendone uno alla volta le bolle non si fondono (ma ci sta)

    for i in range(len(coll)):
        aline=folium.PolyLine(locations=coll[i],weight=coll_molt[i],color = 'blue')
        m.add_child(aline)


    m.save("map.html")
    webbrowser.open("map.html")